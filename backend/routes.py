"""
Flask routes for Bottega Bodega backend.
"""
import os
import uuid
import secrets
from datetime import datetime
from flask import Flask, request, jsonify, g, render_template, send_from_directory, abort
from flask_cors import CORS
import stripe
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from config import Config
from models import init_db, Member, MallratContent, MallratContentDelivery, DiningEvent, EventRSVP, WallEntry, MarvinBallad

# Create Flask app
app = Flask(__name__,
            template_folder='templates',
            static_folder='static',
            static_url_path='/static')
app.config.from_object(Config)

# CORS — allow only the frontend origins
CORS(app, origins=[
    Config.FRONTEND_URL,
    'https://541fa2ac.bodega-aiforlancaster.pages.dev',
    'https://bodega-aiforlancaster.pages.dev',
], methods=['GET', 'POST', 'OPTIONS'], allow_headers=['Content-Type'])

# Stripe init
stripe.api_key = Config.STRIPE_SECRET_KEY

# Price ID → (product_name, unit_amount_cents) mapping
PRICE_MAP = {
    'price_1TSMv5GzXpChNrVvIYnZf7ZG': ('Bottega Bodega — Mallrat Membership', Config.PRICE_MALLRAT),
    'price_1TSMw8GzXpChNrVv7BTIUT0z': ('Bottega Bodega — Idea Dining Club Membership', Config.PRICE_DINING),
    'price_1TSMxwGzXpChNrVvK8mGuDJb': ('Marvin Treat — Pay What You Want', Config.PRICE_MARVIN),
}

# Database setup
engine = init_db()
db_session = scoped_session(sessionmaker(bind=engine))

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

# === HELPERS ===
def generate_token():
    return secrets.token_urlsafe(16)

def send_email(to, subject, html_content, text_content=None):
    pass  # TODO: Resend API

def notify_admin(subject, body):
    pass  # TODO

# === PUBLIC PAGES ===

@app.route('/')
def landing():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/bodega-style.css')
def styles():
    return send_from_directory(app.static_folder, 'bodega-style.css')

@app.route('/icons/<path:filename>')
def icon(filename):
    return send_from_directory(os.path.join(app.static_folder, 'icons'), filename)

@app.route('/terms.html')
def terms():
    return render_template('terms.html')

# === API ROUTES ===

@app.route('/api/create-checkout-session', methods=['POST'])
def create_checkout_session():
    data = request.get_json()
    price_id = data.get('price_id')
    tier = data.get('tier', '')

    if price_id not in PRICE_MAP:
        return jsonify({'error': 'invalid price_id'}), 400

    product_name, unit_amount = PRICE_MAP[price_id]

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{'price': price_id, 'quantity': 1}],
            mode='payment',
            success_url=f"{Config.BODEGA_URL}/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{Config.BODEGA_URL}/",
            metadata={'tier': tier, 'price_id': price_id}
        )
        return jsonify({'url': session.url, 'session_id': session.id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, Config.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return jsonify({'error': 'invalid payload'}), 400
    except stripe.error.SignatureVerificationError:
        return jsonify({'error': 'invalid signature'}), 400

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        tier = session['metadata'].get('tier', '')
        price_id = session['metadata'].get('price_id', '')
        customer_email = session['customer_details']['email']
        payment_id = session['payment_intent']

        member = Member(
            email=customer_email,
            tier=tier,
            stripe_customer_id=session.get('customer'),
            stripe_payment_id=payment_id,
        )
        db_session.add(member)
        db_session.commit()

        if tier == 'mallrat':
            content = db_session.query(MallratContent).filter_by(active=True).first()
            if content:
                token = generate_token()
                delivery = MallratContentDelivery(
                    member_id=member.id,
                    content_id=content.id,
                    access_token=token
                )
                db_session.add(delivery)
                db_session.commit()
        elif tier == 'dining-club':
            ballad = MarvinBallad(
                member_id=member.id,
                prompt=f"Compose a ballad celebrating {customer_email}, newest patron of the Idea Dining Club."
            )
            db_session.add(ballad)
            db_session.commit()
        elif tier == 'marvin-treat':
            pass  # reward logic TBD

        notify_admin('New Bodega Member', f'{tier} — {customer_email}')

    return jsonify({'status': 'ok'}), 200

# === MEMBER AREA === (unchanged body)...
@app.route('/member/<token>')
def member_dashboard(token):
    pass

@app.route('/member/<int:member_id>/content/<token>')
def deliver_content(member_id, token):
    delivery = db_session.query(MallratContentDelivery).filter_by(
        member_id=member_id, access_token=token
    ).first()
    if not delivery:
        abort(404)
    delivery.viewed = True
    db_session.commit()
    content = delivery.content
    return render_template('content_delivery.html', content=content, member=delivery.member)

@app.route('/member/<int:member_id>/wall', methods=['GET', 'POST'])
def member_wall(member_id):
    member = db_session.query(Member).get_or_404(member_id)
    if request.method == 'POST':
        pass
    return render_template('wall_upload.html', member=member)

@app.route('/member/<int:member_id>/ballad/<int:ballad_id>')
def member_ballad(member_id, ballad_id):
    ballad = db_session.query(MarvinBallad).filter_by(id=ballad_id, member_id=member_id).first_or_404()
    return render_template('ballad.html', ballad=ballad)

@app.route('/member/<int:member_id>/events')
def member_events(member_id):
    member = db_session.query(Member).get_or_404(member_id)
    events = db_session.query(DiningEvent).filter_by(is_active=True).all()
    rsvps = {r.event_id for r in member.rsvps}
    return render_template('events.html', member=member, events=events, rsvps=rsvps)

@app.route('/member/<int:member_id>/events/<int:event_id>/rsvp', methods=['POST'])
def rsvp_event(member_id, event_id):
    member = db_session.query(Member).get_or_404(member_id)
    event = db_session.query(DiningEvent).get_or_404(event_id)
    rsvp = EventRSVP(member_id=member.id, event_id=event.id)
    db_session.add(rsvp)
    db_session.commit()
    return jsonify({'status': 'rsvp confirmed'}), 200

# === ADMIN ROUTES ===

@app.route('/admin')
def admin_login():
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if request.args.get('key') != Config.ADMIN_PASSWORD:
        abort(403)
    members = db_session.query(Member).order_by(Member.joined_at.desc()).all()
    ballads = db_session.query(MarvinBallad).filter_by(status='queued').all()
    return render_template('admin_dashboard.html', members=members, ballads=ballads)

@app.route('/admin/content', methods=['GET', 'POST'])
def admin_content():
    if request.args.get('key') != Config.ADMIN_PASSWORD:
        abort(403)
    if request.method == 'POST':
        pass
    contents = db_session.query(MallratContent).all()
    return render_template('admin_content.html', contents=contents)

@app.route('/admin/events', methods=['GET', 'POST'])
def admin_events():
    if request.args.get('key') != Config.ADMIN_PASSWORD:
        abort(403)
    if request.method == 'POST':
        pass
    events = db_session.query(DiningEvent).order_by(DiningEvent.date.desc()).all()
    return render_template('admin_events.html', events=events)

@app.route('/admin/wall')
def admin_wall():
    if request.args.get('key') != Config.ADMIN_PASSWORD:
        abort(403)
    entries = db_session.query(WallEntry).filter_by(is_visible=True).all()
    return render_template('admin_wall.html', entries=entries)

@app.route('/admin/ballad/<int:ballad_id>/fulfill', methods=['POST'])
def fulfill_ballad(ballad_id):
    if request.args.get('key') != Config.ADMIN_PASSWORD:
        abort(403)
    ballad = db_session.query(MarvinBallad).get_or_404(ballad_id)
    return jsonify({'status': 'ballad queued'})

# === HEALTH ===

@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7900, debug=False)

# Bottega Bodega — Setup & Completion Checklist

## What's Built So Far

### A. Frontend (Static Site) — Retro RPG Theme ✓
- **[x]** `landing-page/bodega-index.html` — membership landing page with two-tier cards
- **[x]** `landing-page/bodega-style.css` — complete CSS with CRT scanlines, pixel fonts, gold borders, RPG shop aesthetic
- **[x]** `landing-page/icons/mallrat-icon.png` — 64×64 pixel art: rat peering into display case with glowing object
- **[x]** `landing-page/icons/dining-icon.png` — 64×64 pixel art: two plates sharing central bowl (idea)
- **[x]** `scripts/build_bodega_site.py` — standalone build script that copies assets to `deploy/bodega/`
- **[x]** Updated `scripts/build_site.py` to call bodega builder automatically
- **[x]** Static pages: terms of service

**Visual system:** Press Start 2P + VT323 fonts, dark blue-black (#0f0f1a) with gold (#ffd700) and forest green (#4a7c59), CRT scanline overlay, 4px double borders, pixel-art borders.

### B. Backend (Flask API) — Shelf-Redeemed Scaffold ✓
- **[x]** `backend/models.py` — SQLAlchemy models: members, payments, content, events, wall, ballads
- **[x]** `backend/routes.py` — Flask routes: checkout creation, webhook handler, member dashboard, admin pages
- **[x]** `backend/config.py` — environment-based configuration
- **[x]** `backend/templates/` — admin login, dashboard, content/events/wall management, content delivery page, success page
- **[x]** `backend/requirements.txt` — Python dependencies
- **[x]** `backend/.env.example` — configuration template
- **[x]** Nginx site config: `/tmp/bodega-nginx.conf`
- **[x]** Systemd service: `/tmp/bodega.service`
- **[x]** VPS setup script: `setup_bodega_vps.sh`

### C. Deployment Scripts ✓
- **[x]** Local build script generates `deploy/bodega/` directory
- **[x]** Setup script for VPS (ready to run on arc-vps)

---

## What Remains — Action Items

### I. Stripe Integration (Required Before Launch)

1. **Create Stripe products** in your Stripe dashboard (or use existing account):
   - Product 1: "Bottega Bodega — Mallrat Membership" → $25.00 one-time
   - Product 2: "Bottega Bodega — Idea Dining Club Membership" → $1,000.00 one-time
   - Record: Product IDs and Price IDs

2. **Configure webhook endpoint** in Stripe dashboard:
   - URL: `https://bodega.aiforlancaster.com/api/webhook` (once DNS points to VPS)
   - Events to listen: `checkout.session.completed`
   - Get webhook signing secret → `STRIPE_WEBHOOK_SECRET`

3. **Get API keys**:
   - Publishable key (pk_live_) → `STRIPE_PUBLISHABLE_KEY`
   - Secret key (sk_live_) → `STRIPE_SECRET_KEY`

**Place keys in:** `/opt/bodega-backend/.env` on arc-vps

### II. VPS Deployment (One-time Setup)

**Run these steps on arc-vps:**

```bash
# 1. Transfer backend code
scp -r ~/clawd/local-ai-business/backend arc-vps:/opt/bodega-backend/

# 2. Run setup script
ssh arc-vps "sudo bash /tmp/setup_bodega_vps.sh"

# 3. Install Python deps
ssh arc-vps "source /opt/bodega-backend/venv/bin/activate && pip install -r /opt/bodega-backend/requirements.txt"

# 4. Initialize database
ssh arc-vps "source /opt/bodega-backend/venv/bin/activate && python -c 'from models import init_db; init_db()'"

# 5. Edit .env file
ssh arc-vps "nano /opt/bodega-backend/.env"  # fill in real keys

# 6. Start service
ssh arc-vps "sudo systemctl start bodega-backend"
ssh arc-vps "sudo systemctl status bodega-backend"
```

### III. DNS Configuration (Cloudflare)

1. Add DNS record:
   - Type: `CNAME`
   - Name: `bodega`
   - Target: `arc-vps` IP address (currently `5.161.247.95`) **OR** use Cloudflare Tunnel

2. If using Tunnel (safer, no open ports):
   - Create tunnel in Cloudflare dashboard → arc-vps
   - Public hostname: `bodega.aiforlancaster.com` → `http://localhost:7892`
   - No DNS A record needed, tunnel handles routing

3. Verify propagation:
   ```bash
   dig bodega.aiforlancaster.com +short
   ```

### IV. Content & Data Population

Once backend is live, use admin dashboard:

**Mallrat Content:**
- Upload exactly one piece of content (PDF/image/video) for the first active Mallrat membership
- Write the handwritten-style note (Leo's thoughts)
- Set as `active=True`

**Dining Events:**
- Create the first "Idea Dining Club" event (date, location in River Valley Mall Bodega space)
- Capacity: set a reasonable limit (e.g., 12)
- Description: what the experience is like

**Wall:**
- Prepare placeholder image or upload first test entry

### V. Marvin Ballad Pipeline (Asynchronous Agent)

Two implementation paths:

**Option A — Pre-compute at sign-up (simplest, ✅ recommended):**
- webhook handler creates Marvin ballad record with `status='queued`
- cron job or manual admin trigger runs Marvin agent that:
  1. Loads member context from DB
  2. Composes ballad via Hermes agent (Marvin's voice)
  3. Records audio with `hermes-say.py` using bodega-cat voice
  4. Stores MP3 at `/static/ballads/{member_id}.mp3`
  5. Updates record with `status='complete', audio_url=...`
  6. Sends email with link

**Option B — On-demand by member request:**
- Add `/member/<id>/ballad/request` endpoint
- Same agent pipeline, triggered manually
- Delivered within 24h

**Recommendation:** Option A — instant gratification, simpler timeline. Marvin already exists as an agent; just need a thin orchestration wrapper.

### VI. Email Infrastructure (Resend)

Configure transactional email:
- Welcome email with membership details + content link / event calendar / ballad ETA
- Receipt emails (Stripe can do this, but custom branding better)
- Event reminders (24h before)
- Ballad completion notification

Resend setup: `RESEND_API_KEY` in .env, and `from` address aligned with domain.

---

## Launch Sequence (Day-of)

**T-minus 3 days:**
- [ ] Deploy backend to VPS, start service, test health endpoint
- [ ] Configure Stripe in test mode — run full checkout flow end-to-end
- [ ] Test webhook locally with Stripe CLI, then switch to live mode
- [ ] Add DNS record, wait for propagation (up to 1h)

**T-minus 1 day:**
- [ ] Populate Mallrat content (one piece) + Leo's handwritten note (typed, styled to look handwritten)
- [ ] Create first Dining Event (date 2-3 weeks out, capacity 8-12)
- [ ] Upload first Wall photo (test)
- [ ] Verify email delivery (Resend sandbox/test mode)

**Launch day:**
- [ ] Post on X/Twitter, LinkedIn, YouTube community tab
- [ ] Pin tweet with link
- [ ] Email to existing aiforlancaster.com list (if any)
- [ ] Monitor webhook logs, Stripe dashboard for first sales

---

## Admin Quick-Reference

**Access:** `https://bodega.aiforlancaster.com/admin?key=<ADMIN_PASSWORD>`

**Pages:**
- `/admin/dashboard` — recent members, pending ballads
- `/admin/content` — upload Mallrat content pieces
- `/admin/events` — create Dining Club events
- `/admin/wall` — approve member photos
- `/admin/ballad` — trigger Marvin ballad generation

**Database location:** `/opt/bodega-backend/data/bodega.db`

**Tail logs:** `ssh arc-vps "sudo journalctl -u bodega-backend -f"`

**Restart service:** `ssh arc-vps "sudo systemctl restart bodega-backend"`

---

## Cost Estimate

- **VPS:** Already paid (arc-vps)
- **Stripe fees:** 2.9% + $0.30 per transaction
- **Email (Resend):** First 3,000 emails/month free
- **Cloudflare Pages:** Free tier sufficient
- **Domain:** Already owned (aiforlancaster.com)

---

## Design Notes (Aesthetic Rationale)

*Why retro RPG?* You're building a bodega in a dead mall. Online attention is the mall. The aesthetic telegraphs "this is a collectible, not content." Inventory items, not variables. The pixel art + gold borders + CRT scanlines are deliberate anachronism — a choice to move at pre-Algorithm speeds. It's not dated, it's intentional.

*Color palette rationale:* Dark blue-black background reduces eye strain in dim bodega lighting; gold accents telegraph value; forest green for Mallrat (small, scrappy, out-of-place); deep gold for Dining Club (premium, exclusive).

---

## Next Session Checklist

- [ ] **Approve external actions** (scp to VPS, systemctl runs)
- [ ] Provide Stripe credentials (test keys first)
- [ ] Choose ballad implementation (A or B)
- [ ] Decide Mallrat first content piece + handwritten note copy
- [ ] Set admin password

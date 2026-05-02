# Bottega Bodega — Launch Alignment Summary

Date: May 1, 2026
Source PDF: "Welcome to the Bottega Bodega, the most human place on the internet"
Author: Leo Guinan

---

## What Was Changed

### HTML (landing-page/bodega-index.html)

1. **Title & Meta**
   - Changed `<title>` to "The Bottega Bodega — The Most Human Place on the Internet"
   - Updated meta description to include all three tiers + Marvin Treat

2. **Header Tagline**
   - Changed from "~ Memberships Available ~" → "— The Most Human Place on the Internet —"
   - Matches Substack article headline

3. **Intro Section**
   - Replaced generic "open for business" text with Renaissance bottega framing
   - Added attributed quote: <em>"The most human place on the internet."</em> — Leo Guinan, May 2026
   - Added Marvin bullshit filter reference paragraph

4. **Tiers Intro Paragraph**
   - New paragraph introducing "The Great Online Game" framework
   - Explicitly names Observers and Players
   - Frames Marvin as "your bullshit filter"

5. **Mallrat Tier**
   - Updated subtitle: "Observer Membership — One Content Feature on the Wall"
   - Reframed first feature: "space on the wall for a content recommendation and human blurb by me" (per PDF wording)
   - Added: "You are an <strong>Observer</strong> in the Great Online Game" feature
   - Button text: "Acquire Membership" → "Become an Observer"
   - Added `data-price-id="price_1TSMv5GzXpChNrVvIYnZf7ZG"`

6. **Idea Dining Club Tier**
   - Badge: "PREMIUM" → "PLAYER"
   - Subtitle: "Player Membership — A Seat at the Table" (per PDF: "$1000 gets you a seat at the dining table")
   - Features: bolded Marvin ballad line for emphasis (per PDF: "a ballad written and performed about you by an AI bodega cat")
   - Added: "You are a <strong>Player</strong> in the Great Online Game" feature
   - Added `data-price-id="price_1TSMw8GzXpChNrVv7BTIUT0z"`

7. **Marvin Treat Tier (NEW)**
   - Complete new card with cat emoji icon
   - Subtitle: "Pay What You Want — Random Reward from the Cat"
   - Price display: "$?" with "you decide" period
   - Features emphasize randomness/tip jar nature ("No expectations. Just gratitude, circulated")
   - Button: "Leave a Treat" with `data-price-id="price_1TSMxwGzXpChNrVvK8mGuDJb"`
   - Orange color scheme (Marvin's color)

8. **Footer**
   - Location: "Lancaster, Ohio" → "River Valley Mall, Lancaster, Ohio"
   - Added Marvin quote with Substack link: "Marvin is my bullshit filter."
   - Credit: Leo Guinan, May 2026

9. **JavaScript Checkout Handler**
   - Changed from amount-based to price-id-based checkout
   - `fetch` payload now sends `{tier, price_id: priceId}`
   - Adds loading state (button disabled + "Loading...")
   - Has error fallback with button text restoration per tier
   - Stripe public key placeholder with TODO comment

### CSS (bodega-style.css)

1. `.intro-subtext` — italic attribution styling
2. `.tiers-intro` — wider paragraph for tiers intro text
3. `.tier-card.marvin-treat` — orange border (`#e8871e`) and badge styling
4. `.buy-button.marvin` — orange gradient button matching Marvin theme

---

## PDF Alignment Checklist

- [x] Title: "The most human place on the internet"
- [x] Tagline: "— The Most Human Place on the Internet —"
- [x] Bottega/Renaissance workshop framing
- [x] Location: River Valley Mall, Lancaster, Ohio
- [x] No subscriptions / one-time fees messaging
- [x] Marvin as "bullshit filter" AI
- [x] "The Great Online Game" reference
- [x] Observers / Players role names
- [x] $25 Mallrat = Observer membership, "space on the wall for a content recommendation"
- [x] $1000 Dining Club = Player membership, "seat at the dining table"
- [x] Marvin ballad mention for Dining Club members
- [x] Marvin Treat tier (Pay What You Want) — extra feature beyond PDF but requested
- [x] Substack article attribution in footer

---

## Stripe Price IDs Embedded

| Tier | Price ID |
|------|----------|
| Mallrat | `price_1TSMv5GzXpChNrVvIYnZf7ZG` |
| Marvin Treat | `price_1TSMxwGzXpChNrVvK8mGuDJb` |
| Idea Dining Club | `price_1TSMw8GzXpChNrVv7BTIUT0z` |

---

## Backend Requirements

The backend Flask app (`/api/create-checkout-session`) needs to accept `price_id` in the request body instead of `amount`:

```python
@app.route('/api/create-checkout-session', methods=['POST'])
def create_checkout_session():
    data = request.get_json()
    price_id = data.get('price_id')  # <-- use this instead of amount

    session = stripe.checkout.Session.create(
        mode='payment',
        line_items=[{
            'price': price_id,  # <-- direct price reference
            'quantity': 1,
        }],
        success_url=...,
        cancel_url=...,
    )
    return {'url': session.url}
```

---

## Files Modified

- `landing-page/bodega-index.html` — 223 lines (was 160)
- `landing-page/bodega-style.css` — CSS classes added
- `deploy/bodega/index.html` — auto-updated via build script
- `deploy/bodega/bodega-style.css` — auto-updated via build script

---

## Deployment

To deploy to bodega.aiforlancaster.com:

```bash
cd ~/clawd/local-ai-business
npx wrangler pages deploy ./deploy/bodega --project-name=bodega-aiforlancaster
```

Then configure `bodega.aiforlancaster.com` custom domain in Cloudflare dashboard pointing to that project.

---

**Alignment status: 100%** — site content now mirrors launch announcement messaging, terminology, and Stripe integration.

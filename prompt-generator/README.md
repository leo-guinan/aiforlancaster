# AI Prompt Generator — Integration Plan

## What It Is

A single-page web app where someone types in their business details
(type, name, location, email, differentiator) and gets all 50 prompts
from the book customized with their info. Their business name, type,
and location are pre-filled into every prompt.

Remaining [brackets] (things that change per-use like [paste review]
or [date]) stay highlighted in gold so they know what to fill in.

## What It Gives Us

1. **Email addresses** of people actively using the book
2. **Business type and location** — we learn who our readers are
3. **Differentiator and service** — we learn how they describe themselves
4. **Timestamp** — we see adoption over time
5. **A reason to follow up** — "Hey, you generated prompts 2 weeks ago.
   How's it going? Which ones worked?"

## Deployment

### Cloudflare Pages
- Deploy all site files to a single Cloudflare Pages project
- Domain: aiforlancaster.com
- URL structure:
  - aiforlancaster.com/ → landing page (book + email capture)
  - aiforlancaster.com/prompts → prompt generator
  - aiforlancaster.com/audit → audit worksheet PDF
  - aiforlancaster.com/book → redirect to Amazon listing
  - aiforlancaster.com/call → voice agent info + phone number
- Zero cost hosting, instant deploy

## Backend for Data Collection

The form currently logs to console. We need a real endpoint.

### Simplest option: Google Sheets via Apps Script
1. Create a Google Sheet with columns: timestamp, business_type,
   business_name, location, email, differentiator, service
2. Create a Google Apps Script web app that accepts POST requests
   and appends rows to the sheet
3. Replace the fetch URL in sendToBackend() with the Apps Script URL
4. Total setup time: 30 minutes

### Better option: Beehiiv or Mailchimp
1. When someone submits, add them to the mailing list with tags
   (business_type, location)
2. Tags let you segment later: "send HVAC-specific follow-up to all
   HVAC businesses that used the prompt generator"
3. The email they entered is already their mailing list signup

### Best option: Both
- Google Sheet for the raw data (you can see everything)
- Beehiiv/Mailchimp for the email list (you can send follow-ups)
- One form submission triggers both

## Follow-Up Sequence

### Email 1 (immediate):
Subject: "Your 50 AI prompts are ready"
Body: Link to their generated prompts (or PDF attachment)
Plus: "The book has way more — here's the free PDF"

### Email 2 (Day 3):
Subject: "Did you try any of the prompts?"
Body: "Which ones worked? Which ones didn't? Reply and tell me."
This is the measurement email. Replies = signal.

### Email 3 (Day 7):
Subject: "The $0 AI Audit"
Body: "Now that you've tried the prompts, here's how to find the
bigger opportunities in your business."
Attach: The audit worksheet. Mention the 50% off.

### Email 4 (Day 14):
Subject: "One thing most [business type] owners miss about AI"
Body: Personalized by business type (use Beehiiv/Mailchimp tags).
Specific insight relevant to their industry.
Soft CTA: "If you want to talk through it, my calendar's here."

## Where to Link This

- YouTube shorts: "Get all 50 prompts customized for YOUR business.
  Link in bio." (this is the CTA for every short)
- YouTube Video 1 description
- Book Chapter 3: mention the generator alongside the prompts
- Landing page: add a section or button
- Audit worksheet footer
- Voice agent: when someone calls and asks about prompts, direct
  them to the generator URL

## The Measurement Question

"Are we actually helping anyone?"

How we answer it:
1. **Volume**: How many people generate prompts? (Google Sheet)
2. **Follow-through**: How many reply to Email 2? (Beehiiv)
3. **Conversion**: How many download the audit worksheet? (Email 3 clicks)
4. **Revenue**: How many book assessments? (Cal.com)
5. **Satisfaction**: Direct replies. Did the prompts work for them?

If nobody replies to Email 2, the prompts aren't useful enough.
If lots reply but nobody downloads the audit, the book-to-service
pipeline is broken. Each step is a diagnostic.

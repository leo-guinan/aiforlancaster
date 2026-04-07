# How to Create "AI for [YourTown]"

A step-by-step guide to forking this book and site for your own community.

---

## What You're Getting

This repository contains:
- A complete book manuscript (~30,000 words) about AI for small business
- A website with 6 pillar content guides (2,000+ words each)
- A prompt library, tool comparison charts, and audit worksheets
- Cover design templates
- Deployment configs for static hosting

About 80% of the content is universal. The other 20% is Lancaster-specific
and needs your local research to replace.

---

## Step 1: Fork the Repository

```
git clone https://github.com/leoguinan/ai-for-lancaster.git
mv ai-for-lancaster ai-for-[yourtown]
cd ai-for-[yourtown]
```

## Step 2: Edit town-config.yaml

This is the single source of truth for your town's details:

```yaml
town: [Your Town Name]
state: [Your State]
domain: aifor[yourtown].com
author: [Your Name]
author_email: [your@email.com]
chamber_of_commerce:
  name: [Your Local Chamber]
  phone: [Phone Number]
local_resources:
  - name: [SCORE chapter or SBDC]
    url: [URL]
  - name: [Community college or extension office]
    url: [URL]
joined_network: [YYYY-MM-DD]
```

## Step 3: What to Change in the Book

### Chapters that need LOCAL edits:

| Chapter | What to Change |
|---------|---------------|
| Chapter 1 | Replace "Lancaster" with your town. Update the author bio. |
| Chapter 12 | FULL REWRITE. This is your local resources chapter. Research your town's chamber, SCORE chapter, SBDC, extension office, community college, coworking spaces. |
| Chapter 13 | Light edits only. The "Fork This Book" chapter is mostly universal. |
| Front Matter | Update author name, town name, dedication. |

### Chapters that are UNIVERSAL (minimal or no edits):

| Chapter | Why It's Universal |
|---------|-------------------|
| Chapters 2-11 | AI tools, prompts, audits, voice agents -- these work everywhere. |
| Appendices A-C | Prompt library, tool chart, BS detector -- all universal. |

### The 80/20 rule:
- 80% of the work is already done (the universal content)
- 20% is local research you need to do yourself
- That 20% is what makes your version valuable to YOUR town

## Step 4: Take Your Own Cover Photo

The cover should be a real photo of YOUR Main Street. Not a stock photo.
Not AI-generated. A photo you took, standing on the street.

Tips:
- Golden hour (early morning or late afternoon) for warm light
- Include recognizable local buildings or signage
- Empty or quiet street reads as "honest" not "dead"
- Shoot landscape, crop to portrait for the cover
- Your phone camera is fine. Authenticity beats production value.

Cover dimensions for KDP: 1600 x 2560 pixels (Kindle), or 2560 x 1600
for paperback front only.

## Step 5: Set Up Your Site

We use Cloudflare Pages (free tier is plenty):

1. Create a Cloudflare account at cloudflare.com
2. Buy your domain: aifor[yourtown].com (~$10/year)
3. Connect your GitHub repo to Cloudflare Pages
4. The site auto-deploys on every push

The site structure is pre-built. You just need to:
- Update town references in the HTML/markdown
- Add your cover photo
- Update the email capture form endpoint

## Step 6: Localize the Pillar Content

The 6 guide pages in /site/guides/ are mostly universal, but adding
local examples makes them rank for local search:

- "What Is AI?" -- add a local business example
- "AI Voice Agents" -- mention if any local businesses use them
- "How to Audit" -- reference local business types common in your area
- "Hire a Consultant" -- list any local options (or note the lack of them)

Each local reference you add is a long-tail keyword opportunity.
"AI for plumbers in [YourTown]" is a search nobody is targeting.

## Step 7: Join the Network

Once your site is live:

1. Open a PR to the mothership repo adding your town to /network/directory.yaml
2. Add a link to aiforlancaster.com/network on your site
3. We'll link back to you from the network directory
4. Start submitting monthly traffic reports (see NETWORK-PROTOCOL.md)

That's it. You're in.

## Step 8: Ongoing

- Update tool prices and recommendations quarterly
- Add new local examples as you work with businesses
- Submit monthly traffic reports to the network
- Share what content is working in your town
- The network learns from everyone. That's the point.

---

## FAQ

**Do I need to know how to code?**
Barely. If you can edit a text file and push to GitHub, you can do this.
The site template handles the rest.

**Do I need to be an AI expert?**
No. The book teaches what you need to know. Read it first, then localize it.
If you can explain AI to a local business owner, you know enough.

**Can I charge for my version?**
Yes. CC BY-SA allows commercial use. You can sell physical copies, charge
for workshops based on the content, or use it as a lead magnet. You just
have to credit the original and share your version under the same license.

**What if my town already has one?**
Two versions of the same town is fine. Different authors bring different
perspectives and different local connections. The network benefits from
density too.

**What does Leo get out of this?**
Backlinks to aiforlancaster.com. Network effects. And the satisfaction
of watching a good idea spread. That's it. There's no hidden monetization.

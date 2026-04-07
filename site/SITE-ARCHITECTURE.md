# aiforlancaster.com — Site Architecture & Content Strategy

## Overview

aiforlancaster.com is the mothership site for a network of local "AI for [YourTown]" sites. It does three things:

1. Gives away the full book for free (SEO + trust)
2. Publishes pillar content that ranks for long-tail AI + small business keywords
3. Serves as a template other towns can fork

The entire site is anti-hype. That's not a marketing angle — it's the actual editorial policy. No "10x your revenue." No "revolutionary." No stock photos of robots. Just honest, specific, Midwestern-dry information about what AI actually does for small businesses right now.

---

## Site Map

```
aiforlancaster.com/
├── / (homepage)
├── /book/ (full book, free)
│   ├── /book/chapter-1-ai-gold-rush-main-street/
│   ├── /book/chapter-2-what-ai-actually-is/
│   ├── /book/chapter-3-free-tools-today/
│   ├── /book/chapter-4-email-communication/
│   ├── /book/chapter-5-marketing-without-department/
│   ├── /book/chapter-6-operations/
│   ├── /book/chapter-7-ai-audit/
│   ├── /book/chapter-8-scoring-opportunities/
│   ├── /book/chapter-9-voice-agents/
│   ├── /book/chapter-10-custom-automations/
│   ├── /book/chapter-11-hire-ai-consultant/
│   └── /book/chapter-12-fairfield-county/
├── /guides/ (pillar content)
│   ├── /guides/what-is-ai-small-business/
│   ├── /guides/ai-tools-comparison-2025/
│   ├── /guides/ai-voice-agents-small-business/
│   ├── /guides/how-to-audit-business-for-ai/
│   ├── /guides/ai-marketing-small-business/
│   ├── /guides/hire-ai-consultant-without-getting-burned/
│   ├── /guides/ai-customer-service-small-business/
│   ├── /guides/ai-for-restaurants-2025/
│   ├── /guides/ai-for-retail-stores/
│   └── /guides/ai-automation-small-business/
├── /tools/ (reviews and comparisons)
│   ├── /tools/chatgpt-vs-claude-vs-gemini/
│   ├── /tools/best-ai-phone-answering/
│   ├── /tools/ai-email-tools-small-business/
│   ├── /tools/ai-social-media-tools/
│   ├── /tools/ai-bookkeeping-tools/
│   └── /tools/ai-scheduling-tools/
├── /prompts/ (prompt library, individual pages)
│   ├── /prompts/ (index — all 50 prompts)
│   ├── /prompts/customer-email-response/
│   ├── /prompts/social-media-post-facebook/
│   ├── /prompts/product-description/
│   ├── /prompts/review-response-positive/
│   ├── /prompts/review-response-negative/
│   ├── /prompts/job-posting/
│   ├── /prompts/weekly-newsletter/
│   ├── /prompts/complaint-response/
│   ├── /prompts/price-increase-announcement/
│   └── ... (50 total, each on its own page)
├── /fork/ (create your own site)
│   ├── /fork/ (overview and pitch)
│   ├── /fork/how-it-works/
│   ├── /fork/technical-setup/
│   └── /fork/content-customization/
├── /network/ (directory of towns)
│   ├── /network/ (index with map)
│   ├── /network/lancaster-oh/
│   ├── /network/zanesville-oh/
│   └── ... (grows as towns join)
├── /data/ (collective analytics)
│   ├── /data/ (dashboard overview)
│   ├── /data/what-tools-work/
│   ├── /data/cost-savings-reports/
│   └── /data/adoption-rates/
├── /about/
├── /audit/ (free AI audit worksheet download)
└── /contact/
```

---

## Content Strategy by Section

### /book/ — The Full Book (Free)

**Purpose:** Give away the entire book. Every chapter is its own page for SEO. This is the trust engine — nobody else is doing this. It also creates 12+ indexable pages with substantial content.

**Internal Linking:** Each chapter links to the relevant pillar guide. Each chapter links to next/previous chapters. Sidebar shows full table of contents.

**CTA on every page:** "Want the PDF? Download it. Want to talk about this? Email leo@metaspn.com."

| Chapter | URL Slug | Target Keyword |
|---------|----------|---------------|
| Ch 1 | /book/chapter-1-ai-gold-rush-main-street/ | ai consultants small business |
| Ch 2 | /book/chapter-2-what-ai-actually-is/ | what is ai plain english |
| Ch 3 | /book/chapter-3-free-tools-today/ | free ai tools small business |
| Ch 4 | /book/chapter-4-email-communication/ | ai email small business |
| Ch 5 | /book/chapter-5-marketing-without-department/ | ai marketing small business owner |
| Ch 6 | /book/chapter-6-operations/ | ai business operations |
| Ch 7 | /book/chapter-7-ai-audit/ | ai audit small business |
| Ch 8 | /book/chapter-8-scoring-opportunities/ | where to use ai business |
| Ch 9 | /book/chapter-9-voice-agents/ | ai voice agent small business |
| Ch 10 | /book/chapter-10-custom-automations/ | ai automation small business |
| Ch 11 | /book/chapter-11-hire-ai-consultant/ | hire ai consultant |
| Ch 12 | /book/chapter-12-fairfield-county/ | ai lancaster ohio |

---

### /guides/ — Pillar Content Pages

These are the SEO workhorses. Each targets a long-tail keyword cluster, is 2000+ words, and links to book chapters, tools, and prompts.

---

#### Guide 1: What Is AI? A Plain English Guide for Small Business Owners

- **File:** guides/what-is-ai-small-business.md
- **URL:** /guides/what-is-ai-small-business/
- **Target Keyword:** what is ai for small business
- **Secondary Keywords:** ai explained small business, ai for beginners business owners, artificial intelligence small business plain english
- **Meta Description:** AI explained without the jargon. A plain English guide for small business owners who want to know what AI actually does, what it costs, and whether it's worth it. Written by someone who builds AI systems and publishes his failures.
- **Content Outline:**
  1. What AI actually is (autocomplete, not Terminator)
  2. The three things AI does well right now
  3. The three things AI does poorly right now
  4. What it costs (real numbers)
  5. The five questions to ask before spending a dollar on AI
  6. What to do Monday morning
  7. CTA: Read the full book free

---

#### Guide 2: The Best AI Tools for Small Business in 2025 (Honest Review)

- **File:** guides/ai-tools-comparison-2025.md
- **URL:** /guides/ai-tools-comparison-2025/
- **Target Keyword:** best ai tools small business 2025
- **Secondary Keywords:** ai tools comparison small business, chatgpt vs claude for business, free ai tools business owners
- **Meta Description:** An honest comparison of AI tools for small business in 2025. No affiliate links. No sponsored rankings. Just what works, what doesn't, and what's free. Updated quarterly.
- **Content Outline:**
  1. How we evaluated (no affiliate links, no sponsors)
  2. The free tier: ChatGPT, Claude, Gemini, Copilot
  3. The $20/month tier: what the paid versions add
  4. Specialized tools by category
  5. The tools we don't recommend (and why)
  6. What to actually start with
  7. CTA: Read the full book free

---

#### Guide 3: AI Voice Agents for Small Business: What They Cost and Whether They Work

- **File:** guides/ai-voice-agents-small-business.md
- **URL:** /guides/ai-voice-agents-small-business/
- **Target Keyword:** ai voice agents small business
- **Secondary Keywords:** ai phone answering service business, ai receptionist cost, voice ai for small business
- **Meta Description:** AI voice agents can answer your phone, book appointments, and handle basic customer questions. Here's what they actually cost, how well they work, and whether your business needs one. Honest review from someone who builds them.
- **Content Outline:**
  1. What an AI voice agent actually is
  2. What they can and can't do (specific examples)
  3. Real cost breakdown ($50-500/month range)
  4. Who should get one and who shouldn't
  5. How to test before you buy
  6. The setup process (it's not plug-and-play)
  7. Our honest recommendation
  8. CTA: Read the full book free

---

#### Guide 4: The $0 AI Audit: How to Find Where AI Actually Helps Your Business

- **File:** guides/how-to-audit-business-for-ai.md
- **URL:** /guides/how-to-audit-business-for-ai/
- **Target Keyword:** ai audit small business
- **Secondary Keywords:** where to use ai in my business, ai readiness assessment small business, find ai opportunities business
- **Meta Description:** Walk through your business in one hour and find exactly where AI helps — and where it doesn't. Free worksheet included. No consultant needed. No software to buy.
- **Content Outline:**
  1. Why most "AI readiness assessments" are sales tools
  2. The one-hour walkthrough method
  3. Category 1: Communication and email
  4. Category 2: Marketing and content
  5. Category 3: Operations and scheduling
  6. Category 4: Customer service
  7. Category 5: Bookkeeping and admin
  8. Scoring your opportunities (effort vs. impact)
  9. The free worksheet (download)
  10. CTA: Read the full book free

---

#### Guide 5: AI Marketing for Small Business: What Works, What Doesn't, What's Snake Oil

- **File:** guides/ai-marketing-small-business.md
- **URL:** /guides/ai-marketing-small-business/
- **Target Keyword:** ai marketing small business
- **Secondary Keywords:** ai social media small business, ai content marketing, using ai for business marketing
- **Meta Description:** A no-hype guide to using AI for small business marketing. What actually saves time, what produces garbage, and what's a complete waste of money. Real examples from real businesses.
- **Content Outline:**
  1. The honest truth: AI won't replace your marketing judgment
  2. What works: social media content batching
  3. What works: email drafting and response
  4. What works: review responses
  5. What doesn't work: AI-generated blog posts (usually)
  6. What's snake oil: "AI marketing agencies"
  7. The one-hour-per-week system
  8. Platform-specific prompts you can copy
  9. CTA: Read the full book free

---

#### Guide 6: How to Hire an AI Consultant Without Getting Burned

- **File:** guides/hire-ai-consultant-without-getting-burned.md
- **URL:** /guides/hire-ai-consultant-without-getting-burned/
- **Target Keyword:** hire ai consultant small business
- **Secondary Keywords:** ai consultant red flags, how to hire ai expert, ai consulting cost small business
- **Meta Description:** 800,000 people are about to call themselves AI consultants. Here's how to tell the good ones from the bad ones, what to pay, and what to demand in a contract. Written by an AI consultant who'll tell you when you don't need one.
- **Content Outline:**
  1. The gold rush is here (800,000 new "consultants")
  2. The five red flags (specific, checkable)
  3. The five green flags
  4. What to pay (real ranges by project type)
  5. What to demand in a contract
  6. When you DON'T need a consultant
  7. The questions to ask in the first meeting
  8. CTA: Read the full book free

---

#### Guide 7: AI Customer Service for Small Business (Future)

- **File:** guides/ai-customer-service-small-business.md
- **URL:** /guides/ai-customer-service-small-business/
- **Target Keyword:** ai customer service small business
- **Secondary Keywords:** ai chatbot small business, automated customer service, ai help desk small business
- **Meta Description:** Can AI handle your customer service? Sometimes. Here's when it works, when it backfires, and how to set it up without annoying your customers.
- **Content Outline:**
  1. What AI customer service actually looks like in 2025
  2. Chatbots vs. voice agents vs. email automation
  3. The "warm handoff" model (AI handles simple, humans handle complex)
  4. Cost breakdown by approach
  5. Setup guide for each option
  6. When to skip it entirely
  7. CTA: Read the full book free

---

#### Guide 8: AI for Restaurants in 2025 (Future)

- **File:** guides/ai-for-restaurants-2025.md
- **URL:** /guides/ai-for-restaurants-2025/
- **Target Keyword:** ai for restaurants 2025
- **Secondary Keywords:** ai restaurant ordering, ai restaurant marketing, ai tools restaurants
- **Meta Description:** A practical guide to AI for restaurant owners. Phone ordering, menu optimization, review management, and marketing — what's worth it and what's not. No hype.
- **Content Outline:**
  1. The restaurant-specific AI landscape
  2. Phone ordering and reservations (voice agents)
  3. Review management on autopilot
  4. Social media content that doesn't feel robotic
  5. Menu analysis and pricing
  6. What to skip
  7. CTA: Read the full book free

---

#### Guide 9: AI for Retail Stores (Future)

- **File:** guides/ai-for-retail-stores.md
- **URL:** /guides/ai-for-retail-stores/
- **Target Keyword:** ai for retail stores 2025
- **Content Outline:** (TBD — inventory, product descriptions, customer communication)

---

#### Guide 10: AI Automation for Small Business (Future)

- **File:** guides/ai-automation-small-business.md
- **URL:** /guides/ai-automation-small-business/
- **Target Keyword:** ai automation small business
- **Content Outline:** (TBD — Zapier/Make integrations, workflow automation, when custom vs. off-shelf)

---

### /tools/ — Tool Reviews and Comparisons

**Purpose:** Rank for "[tool] review" and "[tool] vs [tool]" queries. No affiliate links — ever. That's the trust signal.

| Page | Target Keyword | Status |
|------|---------------|--------|
| /tools/chatgpt-vs-claude-vs-gemini/ | chatgpt vs claude vs gemini business | Planned |
| /tools/best-ai-phone-answering/ | best ai phone answering service | Planned |
| /tools/ai-email-tools-small-business/ | ai email tools small business | Planned |
| /tools/ai-social-media-tools/ | ai social media tools small business | Planned |
| /tools/ai-bookkeeping-tools/ | ai bookkeeping small business | Planned |
| /tools/ai-scheduling-tools/ | ai scheduling tools | Planned |

**Template for each tool page:**
- What it does (one paragraph)
- What it costs (table: free/paid tiers)
- What it's good at (specific tasks)
- What it's bad at (specific failures)
- Who should use it (business type)
- Who should skip it
- Our rating: Worth It / Maybe / Skip It

---

### /prompts/ — The Prompt Library

**Purpose:** The 50 prompts from the book, each on its own page for SEO. Target long-tail "ai prompt for [task]" queries.

**Template for each prompt page:**
- The prompt (copy-paste ready)
- What it's for (one sentence)
- How to customize it (variables to change)
- Example output
- Tips for better results
- Related prompts (internal links)

**Sample prompt pages:**
| Page | Target Keyword |
|------|---------------|
| /prompts/customer-email-response/ | ai prompt customer email |
| /prompts/social-media-post-facebook/ | ai prompt facebook post business |
| /prompts/product-description/ | ai prompt product description |
| /prompts/review-response-positive/ | how to respond to positive review ai |
| /prompts/review-response-negative/ | how to respond to negative review ai |
| /prompts/job-posting/ | ai prompt job posting |
| /prompts/weekly-newsletter/ | ai prompt newsletter |
| /prompts/price-increase-announcement/ | price increase announcement template |
| /prompts/complaint-response/ | ai prompt customer complaint |
| /prompts/meeting-agenda/ | ai prompt meeting agenda |

---

### /fork/ — Create Your Own AI for [YourTown]

**Purpose:** This is how the network grows. Explain the model, provide the tools, make it easy.

**Pages:**
- **/fork/** — The pitch: Why your town needs this. The model (free book + local trust + network effects). Who should do it (local person, not a consultant from Columbus).
- **/fork/how-it-works/** — The business model. How the network benefits everyone. What you get (content, templates, analytics). What you contribute (local knowledge, local presence).
- **/fork/technical-setup/** — Step-by-step: Fork the repo, customize the content, deploy. Assumes no technical background — or points to someone in the network who can help.
- **/fork/content-customization/** — How to localize the book. What to change (town names, local businesses, county-specific info). What to keep (the core advice doesn't change).

---

### /network/ — Directory of Towns

**Purpose:** Social proof + internal linking + local SEO for each town.

**Index page:** Map of all active towns. Stats (how many businesses reached, how many tools adopted, collective savings). Link to each town's site.

**Each town page (/network/[town-slug]/):**
- Town overview (population, top industries, business count)
- Local champion (who runs it)
- Local stats (if available)
- Link to their site

---

### /data/ — Collective Analytics Dashboard

**Purpose:** Transparency. Show what's working across the network. This is unique — nobody else publishes this data.

**Pages:**
- **/data/** — Overview dashboard. Key metrics across all towns.
- **/data/what-tools-work/** — Aggregated tool adoption and satisfaction data from network members.
- **/data/cost-savings-reports/** — Real numbers from real businesses. Anonymized but specific.
- **/data/adoption-rates/** — What percentage of businesses that read the book actually implement something? What do they implement first?

---

## Internal Linking Strategy

Every piece of content links to at least three other pieces:

1. **Guide → Book chapters:** "Want to go deeper? Read Chapter 7 of the free book."
2. **Guide → Tools:** "We compare these tools in detail at /tools/chatgpt-vs-claude-vs-gemini/"
3. **Guide → Prompts:** "Copy the exact prompt at /prompts/customer-email-response/"
4. **Book chapters → Guides:** "For an updated version of this advice, see our guide on AI marketing."
5. **Prompts → Guides:** "Learn the strategy behind this prompt in our marketing guide."
6. **Everything → /fork/:** Footer link on every page: "Want this for your town?"

---

## Technical SEO Notes

- **Schema markup:** FAQ schema on guides, Book schema on chapters, HowTo schema on audit guide
- **Canonical URLs:** Book chapters canonical to site (not PDF)
- **Meta descriptions:** Hand-written for every page, not auto-generated
- **OG images:** Custom for each guide (simple, text-based, no stock photos)
- **Sitemap:** Auto-generated, submitted to GSC
- **Page speed:** Static site (Astro or Next.js static export), no bloat
- **Mobile:** Every page must read well on a phone — that's how most business owners will find it

---

## Content Calendar (First 90 Days)

**Week 1-2:** Launch site with all book chapters + 6 core guides
**Week 3-4:** Publish first 20 prompt pages + 2 tool comparison pages
**Week 5-6:** Publish remaining 30 prompt pages + 2 more tool comparisons
**Week 7-8:** Publish /fork/ section + first network town pages
**Week 9-12:** Publish industry-specific guides (restaurants, retail) + /data/ dashboard

**Ongoing:** Update tool comparisons quarterly. Publish new guides monthly. Add network towns as they join.

---

## Success Metrics

- Organic traffic to guide pages (target: 500 visits/month per guide within 6 months)
- Book chapter page reads (target: 100 complete book reads/month)
- Prompt page traffic (target: high-volume, low-effort pages)
- Fork conversions (target: 5 new towns in first 6 months)
- Email list growth from book/audit downloads
- Zero metric: revenue from the site itself (this is a public good, not a business)

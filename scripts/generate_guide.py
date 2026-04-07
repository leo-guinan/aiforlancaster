#!/usr/bin/env python3
"""
Generate a new guide page for aiforlancaster.com using Claude.
Usage: python generate_guide.py [--slug <slug>] [--dry-run]

Picks the next unbuilt guide from the queue, generates content,
writes it to site/guides/<slug>.md, then calls build_site.py.
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path
from datetime import datetime

SITE_ROOT = Path(__file__).parent.parent
GUIDES_SRC = SITE_ROOT / "site" / "guides"
QUEUE_FILE = SITE_ROOT / "site" / "guides-queue.json"
MANIFEST_FILE = SITE_ROOT / "site" / "guides-manifest.json"

# Guide queue — ordered by SEO priority
# Each entry: slug, title, keyword, description outline
GUIDE_QUEUE = [
    {
        "slug": "ai-customer-service-small-business",
        "title": "AI Customer Service for Small Business: Chatbots, Voice, and When to Skip It",
        "keyword": "ai customer service small business",
        "outline": [
            "What AI customer service actually looks like in 2026 (not sci-fi, not magic)",
            "Chatbots vs. voice agents vs. email automation — which does what",
            "The warm handoff model: AI handles simple, humans handle complex",
            "Real cost breakdown by approach ($0-500/month range)",
            "Setup guide for each option — no technical background assumed",
            "When to skip it entirely (and what to do instead)",
            "Red flags in AI customer service vendors",
        ]
    },
    {
        "slug": "ai-for-restaurants",
        "title": "AI for Restaurants in 2026: What Works, What's Hype, What to Try First",
        "keyword": "ai for restaurants 2026",
        "outline": [
            "The restaurant-specific AI landscape — what's actually useful",
            "Phone ordering and reservations: AI voice agents in practice",
            "Review management on autopilot (Google, Yelp, TripAdvisor)",
            "Social media content that doesn't feel robotic",
            "Menu analysis and pricing decisions",
            "What to skip (the overpriced stuff)",
            "Start here: one thing you can do this week for free",
        ]
    },
    {
        "slug": "ai-for-retail-stores",
        "title": "AI for Retail Stores: Inventory, Customer Service, and Marketing That Actually Works",
        "keyword": "ai for retail stores 2026",
        "outline": [
            "What retail AI actually means in practice",
            "Inventory and product description automation",
            "Customer service chatbots: what they can and can't do",
            "Social media and email marketing with AI",
            "Product photography and listings (AI tools that help)",
            "What to skip",
            "Start here: one free thing this week",
        ]
    },
    {
        "slug": "ai-automation-small-business",
        "title": "AI Automation for Small Business: Zapier, Make, and When to Go Custom",
        "keyword": "ai automation small business",
        "outline": [
            "What automation actually means (vs. AI hype)",
            "The automation stack: Zapier, Make, and native integrations",
            "10 automations every small business can implement today",
            "When off-the-shelf automation breaks down",
            "When to go custom (and what it costs)",
            "The ROI calculation: is it worth it?",
            "Start here: the one automation that pays for itself",
        ]
    },
    {
        "slug": "chatgpt-vs-claude-vs-gemini-small-business",
        "title": "ChatGPT vs. Claude vs. Gemini for Small Business (Honest 2026 Comparison)",
        "keyword": "chatgpt vs claude vs gemini business",
        "outline": [
            "Why this comparison matters (and why most comparisons are useless)",
            "How we evaluated: real small business tasks, not benchmarks",
            "ChatGPT: what it's good at, what it's bad at, what it costs",
            "Claude: what it's good at, what it's bad at, what it costs",
            "Gemini: what it's good at, what it's bad at, what it costs",
            "Head-to-head on the tasks you actually do: emails, social, customer service",
            "Our recommendation by use case",
            "The free tier reality check",
        ]
    },
    {
        "slug": "best-ai-phone-answering-service",
        "title": "The Best AI Phone Answering Services for Small Business (2026 Review)",
        "keyword": "best ai phone answering service",
        "outline": [
            "What AI phone answering actually does (and doesn't do)",
            "How we evaluated: real calls, real businesses",
            "The main players: Vonage AI, Smith.ai, Goodcall, and others",
            "What they cost (table: per minute vs. flat rate)",
            "What works well across all of them",
            "Where they all fall short",
            "Who should use AI phone answering and who shouldn't",
            "Setup: easier than you think, with caveats",
        ]
    },
    {
        "slug": "ai-for-contractors",
        "title": "AI for Contractors and Tradespeople: Estimates, Scheduling, and Customer Follow-Up",
        "keyword": "ai for contractors small business",
        "outline": [
            "The contractor AI use cases that actually matter",
            "Estimate writing and follow-up automation",
            "Scheduling and dispatch (voice agents for inbound calls)",
            "Customer communication: from inquiry to invoice",
            "Reviews and reputation management",
            "What to skip",
            "Start here: the one tool that saves a contractor 2+ hours per week",
        ]
    },
    {
        "slug": "ai-for-law-offices",
        "title": "AI for Small Law Offices: What's Legal, What's Useful, What's Risky",
        "keyword": "ai for small law offices",
        "outline": [
            "The special situation for law offices (ethics, confidentiality, liability)",
            "What AI can do without legal risk: drafts, research, admin",
            "What AI cannot do: give legal advice, substitute for judgment",
            "Client intake automation",
            "Document drafting and review assistance",
            "Billing and time-tracking tools with AI",
            "The confidentiality question: where your data goes",
            "Practical starting point for a small firm",
        ]
    },
    {
        "slug": "ai-for-medical-offices",
        "title": "AI for Medical and Dental Offices: HIPAA, Scheduling, and What to Avoid",
        "keyword": "ai for medical offices small business",
        "outline": [
            "HIPAA and AI: the non-negotiables",
            "Scheduling and appointment reminders (the safe, high-value starting point)",
            "Patient communication automation that's HIPAA-compliant",
            "Transcription and documentation tools",
            "Billing and coding assistance",
            "What to never put into a general AI tool",
            "Vendors to look at (and what to ask them)",
        ]
    },
    {
        "slug": "ai-for-real-estate-agents",
        "title": "AI for Real Estate Agents: Listings, Lead Nurture, and What the NAR Won't Tell You",
        "keyword": "ai for real estate agents",
        "outline": [
            "The real estate AI landscape in 2026",
            "Listing descriptions that don't sound AI-generated",
            "Lead nurture email sequences",
            "Social media content at scale",
            "CRM automation and follow-up",
            "Virtual tours and photography tools",
            "The fair housing question: AI and bias in real estate",
            "Start here: one hour setup, one week of content",
        ]
    },
    {
        "slug": "how-to-use-chatgpt-for-business",
        "title": "How to Actually Use ChatGPT for Your Business (Not the Demo Version)",
        "keyword": "how to use chatgpt for business",
        "outline": [
            "Why most people use ChatGPT wrong",
            "The prompt framework that actually works: Context, Task, Format, Constraints",
            "10 real business prompts you can copy today",
            "How to get consistent results (saving prompts, custom instructions)",
            "What to never put in ChatGPT",
            "When to pay for the $20/month version and when not to",
            "Building it into your actual workflow (not just for experiments)",
        ]
    },
    {
        "slug": "ai-for-accounting-bookkeeping",
        "title": "AI for Small Business Accounting and Bookkeeping: What Saves Time, What Causes Errors",
        "keyword": "ai for small business accounting",
        "outline": [
            "The accounting AI landscape: what's actually useful",
            "AI features in QuickBooks, Xero, and FreshBooks",
            "Receipt scanning and categorization (where it works)",
            "Invoice automation",
            "Tax preparation: what AI can and can't do",
            "When AI makes accounting errors (and how to catch them)",
            "When to use a human accountant",
        ]
    },
    {
        "slug": "ai-social-media-small-business",
        "title": "AI for Social Media: How to Batch a Month of Content in One Afternoon",
        "keyword": "ai social media small business",
        "outline": [
            "Why most AI social media content looks AI-generated (and how to avoid it)",
            "The content batching system: one afternoon, 30 days of posts",
            "Platform by platform: what works on Facebook, Instagram, and Google Business",
            "The editing step that makes the difference",
            "Scheduling tools that actually work",
            "Engagement: what to automate and what to do yourself",
            "The one-hour-per-week maintenance routine",
        ]
    },
    {
        "slug": "ai-email-tools-small-business",
        "title": "AI Email Tools for Small Business: What Saves Time Without Sounding Like a Robot",
        "keyword": "ai email tools small business",
        "outline": [
            "The email problem for small business owners",
            "AI drafting vs. AI-sent (important distinction)",
            "Tools that help with drafting: Gmail AI, Outlook Copilot, Claude",
            "Email automation tools: Klaviyo, Mailchimp AI features",
            "Customer service email automation",
            "The voice problem: keeping it you",
            "What we use and recommend",
        ]
    },
    {
        "slug": "ai-for-home-services",
        "title": "AI for Home Services Businesses: From First Call to Five-Star Review",
        "keyword": "ai for home services business",
        "outline": [
            "The home services AI opportunity (and why most owners haven't touched it)",
            "Inbound call handling: voice agents for HVAC, plumbing, electrical",
            "Estimate follow-up automation",
            "Appointment reminders and day-of communication",
            "Review generation after job completion",
            "Seasonal marketing automation",
            "Start here: the setup that pays back in the first month",
        ]
    },
    {
        "slug": "ai-scheduling-tools",
        "title": "AI Scheduling Tools for Small Business: Calendly, Acuity, and What the AI Actually Does",
        "keyword": "ai scheduling tools small business",
        "outline": [
            "What AI scheduling actually means vs. regular online booking",
            "The main tools: Calendly, Acuity, Booksy, and others",
            "What the AI features actually do (reminder automation, rescheduling, no-shows)",
            "Integration with your phone and email",
            "What it costs vs. what it saves",
            "The setup: easier than you think",
            "Who should and shouldn't bother",
        ]
    },
    {
        "slug": "ai-for-nonprofits",
        "title": "AI for Small Nonprofits: Grants, Communications, and Doing More with Less",
        "keyword": "ai for small nonprofits",
        "outline": [
            "The nonprofit AI reality check",
            "Grant writing assistance: what AI helps with, what it can't do",
            "Donor communications and email automation",
            "Event planning and promotion",
            "Social media and content at scale",
            "Volunteer coordination tools",
            "Free and low-cost options for budget-constrained organizations",
        ]
    },
    {
        "slug": "ai-content-marketing-local-business",
        "title": "AI Content Marketing for Local Businesses: How to Rank in Your City Without an Agency",
        "keyword": "ai content marketing local business",
        "outline": [
            "Why local content is different (and easier) than national SEO",
            "The local keyword opportunity: 'AI for [your town]' and similar",
            "AI-assisted blog posts that actually rank",
            "Google Business Profile optimization with AI",
            "Local link building strategies that work in small cities",
            "The content calendar: one hour a week",
            "Measuring what works (Google Search Console, no fancy tools needed)",
        ]
    },
    {
        "slug": "ai-tools-free-tier-guide",
        "title": "The Real Free Tier: What You Actually Get From ChatGPT, Claude, and Gemini for Free",
        "keyword": "free ai tools for business",
        "outline": [
            "Why the free tiers matter more than paid for most small businesses",
            "ChatGPT free: what you get, what the limits are",
            "Claude free: what you get, what the limits are",
            "Gemini free: what you get, what the limits are",
            "Copilot free (Microsoft): what's included if you have Microsoft 365",
            "The free tier workflow: what you can do without paying a dollar",
            "When it's worth paying $20/month",
        ]
    },
    {
        "slug": "ai-for-salons-spas",
        "title": "AI for Salons and Spas: Booking, Marketing, and Client Retention on Autopilot",
        "keyword": "ai for salons and spas",
        "outline": [
            "The salon/spa AI opportunity",
            "Online booking with AI-powered reminders and no-shows",
            "Client retention: rebooking automation",
            "Social media content: before/after, promotions, local",
            "Review generation and response",
            "Email marketing to existing clients",
            "Start here: the one tool that makes the biggest difference",
        ]
    },
]


def get_built_slugs():
    manifest_path = MANIFEST_FILE
    if not manifest_path.exists():
        return set()
    data = json.loads(manifest_path.read_text())
    return {g['slug'] for g in data}


def get_next_guide(slug=None):
    built = get_built_slugs()
    if slug:
        for g in GUIDE_QUEUE:
            if g['slug'] == slug:
                return g
        print(f"Slug '{slug}' not found in queue")
        return None
    for g in GUIDE_QUEUE:
        if g['slug'] not in built:
            return g
    print("All guides in queue are already built.")
    return None


def generate_guide_content(guide):
    """Call Claude via hermes to generate guide content."""
    outline_text = '\n'.join(f'- {item}' for item in guide['outline'])
    today = datetime.now().strftime('%Y-%m-%d')

    prompt = f"""Write a comprehensive, honest guide for small business owners on the topic: "{guide['title']}"

Target keyword: {guide['keyword']}

The site is aiforlancaster.com — run by Leo Guinan, who builds AI systems in Lancaster, Ohio. His track record is 42% (he publishes misses). The editorial policy is anti-hype: no "10x your revenue", no stock photos of robots, no affiliate links. Just honest, specific information about what AI actually does.

Voice: Midwestern-dry. Direct. Specific numbers when possible. Admits uncertainty. Like explaining it at a bar in Lancaster, not a TED talk.

Cover these sections in order:
{outline_text}

Format requirements:
- Output raw markdown with frontmatter (title, description, keywords as a single comma-separated string NOT a YAML list, author, date)
- Use ## for main sections, ### for subsections
- 1800-2500 words total
- Real numbers, real examples, real trade-offs
- End with a brief "Start Here" section: one specific action they can take this week, for free
- No hype. No "revolutionary". No "game-changing". No "unlock your potential".
- Lancaster/Fairfield County references where they fit naturally (don't force it)

Start with the frontmatter block, then the content.
"""

    # Write prompt to temp file and call claude
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(prompt)
        prompt_file = f.name

    result = subprocess.run(
        ['claude', '-p', prompt],
        capture_output=True,
        text=True,
        timeout=120
    )

    os.unlink(prompt_file)

    if result.returncode != 0:
        print(f"Claude error: {result.stderr}")
        return None

    return result.stdout.strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--slug', help='Specific guide slug to generate')
    parser.add_argument('--dry-run', action='store_true', help='Print what would be done, no writes')
    parser.add_argument('--list', action='store_true', help='List all guides in queue and their status')
    args = parser.parse_args()

    if args.list:
        built = get_built_slugs()
        print(f"\nGuide queue ({len(GUIDE_QUEUE)} total, {len(built)} built):\n")
        for g in GUIDE_QUEUE:
            status = '[BUILT]' if g['slug'] in built else '[QUEUED]'
            print(f"  {status} {g['slug']}")
        print()
        return

    guide = get_next_guide(args.slug)
    if not guide:
        return

    print(f"\nGenerating: {guide['title']}")
    print(f"Slug: {guide['slug']}")

    if args.dry_run:
        print("[dry-run] Would generate and write to:")
        print(f"  {GUIDES_SRC / guide['slug']}.md")
        print(f"  Then run build_site.py")
        return

    print("Calling Claude...")
    content = generate_guide_content(guide)
    if not content:
        print("Generation failed.")
        sys.exit(1)

    # Write the markdown file
    out_path = GUIDES_SRC / f"{guide['slug']}.md"
    out_path.write_text(content)
    print(f"Wrote {out_path}")

    # Run the site builder
    print("Building site...")
    result = subprocess.run(
        [sys.executable, str(Path(__file__).parent / 'build_site.py')],
        cwd=str(SITE_ROOT)
    )
    if result.returncode != 0:
        print("Build failed.")
        sys.exit(1)

    print(f"\nDone. New guide: /guides/{guide['slug']}/")


if __name__ == '__main__':
    main()

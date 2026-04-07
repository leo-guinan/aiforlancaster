# Scripts — The aiforlancaster.com Pipeline

Three scripts run the entire site. You don't need to touch any of them to fork the project — but if you want to run the SEO pipeline, here's how.

---

## build_site.py

**What it does:** Converts all guide markdown files into HTML pages, rebuilds the homepage, generates sitemap.xml, and inserts contextual internal links between guides.

**Run it:**
```bash
python3 scripts/build_site.py
```

**What it produces:**
- `deploy/guides/<slug>/index.html` — one page per guide
- `deploy/guides/index.html` — guides index page
- `deploy/index.html` — homepage (rebuilt from `landing-page/index.html`)
- `deploy/style.css` — shared stylesheet
- `deploy/sitemap.xml` — full sitemap (submit to Google Search Console)
- `site/guides-manifest.json` — list of all built guides (used by generate_guide.py)

**Run this every time you:**
- Add or edit a guide markdown file
- Change the homepage template
- Want to rebuild internal links after adding new guides

**Auto-linking:** The builder automatically links relevant phrases in guide bodies to other guides. For example, "voice agents" in any guide links to the voice agents guide. Rules: max 4 auto-links per page, 1 per target guide, never inside headings or existing links. To add anchor phrases for a new guide, edit the `ANCHOR_PHRASES` dict in `build_link_index()`.

---

## generate_guide.py

**What it does:** Generates a new guide page using Claude CLI, writes the markdown to `site/guides/`, then calls `build_site.py` to rebuild.

**Prerequisites:** Claude CLI installed and authenticated (`claude --version`).

**Run it:**
```bash
# Generate the next guide in the queue
python3 scripts/generate_guide.py

# Generate a specific guide by slug
python3 scripts/generate_guide.py --slug ai-for-restaurants

# See what's in the queue and what's been built
python3 scripts/generate_guide.py --list

# Dry run (shows what would happen, no writes)
python3 scripts/generate_guide.py --dry-run
```

**The queue:** `GUIDE_QUEUE` in `generate_guide.py` is a list of 20 guides with slugs, titles, target keywords, and section outlines. The script picks the first unbuilt slug, generates ~2000 words of content, and adds it to the site.

**Customizing for your town:** Edit the `GUIDE_QUEUE` list to add industry-specific guides relevant to your area. The prompt instructs Claude to reference your town naturally — update the prompt in `generate_guide_content()` to use your town name.

**Daily cron:** The repo is set up to run this daily via a scheduled job. Each day one new guide is generated, built, committed to git, and deployed to Cloudflare Pages automatically.

---

## trends_agent.py

**What it does:** Pulls rising search trends in your area and top posts from relevant subreddits. Runs weekly and saves a JSON snapshot.

**Prerequisites:**
```bash
pip3 install pytrends certifi
```

**Run it:**
```bash
# Print report to terminal
python3 scripts/trends_agent.py

# Save JSON snapshot to data/trends/YYYY-MM-DD.json
python3 scripts/trends_agent.py --save

# Quiet mode (JSON only, no terminal output)
python3 scripts/trends_agent.py --save --quiet
```

**Data sources:**
1. **Google Trends (pytrends)** — rising queries for AI/small business terms in your state. Note: Google Trends resolves to DMA level (metro area), not city level. If you're in a small town, you'll get the nearest major metro.
2. **Reddit** — top posts this week from r/smallbusiness, r/AIBusiness, and your local subreddit. Edit `SUBREDDITS` in the script to add yours.

**Google Search Console:** The script has a placeholder for GSC data. Once you verify your domain in GSC and wire up the API credentials, you'll get actual query data from your site — which queries people used to find you, what pages they landed on, click-through rates. That's the most valuable signal.

**Customizing:**
- `SEED_TERMS` — terms to track interest over time
- `RISING_SEEDS` — broader terms to find rising related queries
- `SUBREDDITS` — add your local community subreddit
- `RELEVANCE_KEYWORDS` — terms used to filter Reddit posts for relevance
- `OHIO_GEO` — change to your state code (e.g., `US-TX`, `US-PA`)

---

## Running the full pipeline

```bash
# 1. Generate a new guide
python3 scripts/generate_guide.py

# 2. Build the site (called automatically by generate_guide.py, but also run manually after edits)
python3 scripts/build_site.py

# 3. Deploy
npx wrangler pages deploy ./deploy --project-name=your-project-name

# 4. Commit
git add -A && git commit -m "Add new guide: <slug>" && git push
```

---

## Dependencies

| Package | Used by | Install |
|---------|---------|---------|
| pytrends | trends_agent.py | `pip3 install pytrends` |
| certifi | trends_agent.py | `pip3 install certifi` |
| Claude CLI | generate_guide.py | [docs.anthropic.com/claude-code](https://docs.anthropic.com/claude-code) |
| wrangler | deployment | `npm install -g wrangler` |

Python stdlib only for `build_site.py` — no dependencies.

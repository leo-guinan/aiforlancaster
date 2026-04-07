#!/usr/bin/env python3
"""
Lancaster / Columbus DMA Trends Agent
======================================
Surfaces rising search trends relevant to small business + AI in the Columbus
metro area (which includes Lancaster / Fairfield County).

Data sources:
  1. pytrends  — Google Trends rising queries + interest over time (Columbus DMA / Ohio)
  2. Reddit    — r/Lancaster, r/Columbus, r/smallbusiness: top posts this week
  3. GSC       — (future) aiforlancaster.com query data once GSC API is wired up

Run:
  python3 trends_agent.py                  # print report to stdout
  python3 trends_agent.py --save           # also write JSON to data/trends/
  python3 trends_agent.py --save --quiet   # JSON only, no stdout

Cron: called by the daily cron job, output delivered to Telegram.
"""

import argparse
import json
import time
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# ── Dependencies ──────────────────────────────────────────────────────────────
try:
    from pytrends.request import TrendReq
except ImportError:
    print("pip3 install pytrends")
    sys.exit(1)

try:
    import urllib.request
    import urllib.parse
except ImportError:
    pass

# ── Config ────────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data" / "trends"

# Columbus DMA — covers Lancaster, Zanesville, Chillicothe
OHIO_GEO = "US-OH"

# Topics to track: mix of AI, small business, local economy signals
SEED_TERMS = [
    "AI for business",
    "chatgpt",
    "voice agent",
    "small business automation",
    "AI assistant",
]

# Rising query seeds — broader, to catch what the market is moving toward
RISING_SEEDS = [
    "AI",
    "automation",
    "small business",
]

# Subreddits to monitor
SUBREDDITS = ["lancaster", "Columbus", "smallbusiness", "AIBusiness"]

# Small-business relevance filter keywords
RELEVANCE_KEYWORDS = [
    "business", "small business", "local", "restaurant", "retail", "contractor",
    "lawyer", "accountant", "dentist", "doctor", "salon", "shop", "store",
    "ai", "chatgpt", "automation", "voice", "phone", "customer", "marketing",
    "seo", "website", "google", "review", "revenue", "client", "customer",
    "ohio", "lancaster", "fairfield", "columbus",
]


# ── Pytrends helpers ──────────────────────────────────────────────────────────

def get_pytrends_client():
    return TrendReq(hl='en-US', tz=300, timeout=(15, 30))


def fetch_rising_queries(pt, seed_term, geo=OHIO_GEO, timeframe='now 7-d'):
    """Return list of rising query dicts for a seed term."""
    try:
        pt.build_payload(kw_list=[seed_term], timeframe=timeframe, geo=geo)
        time.sleep(2)
        rq = pt.related_queries()
        rising = rq.get(seed_term, {}).get('rising')
        if rising is not None and not rising.empty:
            return rising[['query', 'value']].to_dict('records')
    except Exception as e:
        print(f"  pytrends error ({seed_term}): {e}", file=sys.stderr)
    return []


def fetch_interest_over_time(pt, terms, geo=OHIO_GEO, timeframe='now 7-d'):
    """Return weekly interest index for each term."""
    try:
        pt.build_payload(kw_list=terms, timeframe=timeframe, geo=geo)
        time.sleep(2)
        df = pt.interest_over_time()
        if df.empty:
            return {}
        # Last 7 days average vs prior 7 days average → trend direction
        result = {}
        for term in terms:
            if term in df.columns:
                vals = df[term].tolist()
                mid = len(vals) // 2
                recent = sum(vals[mid:]) / max(len(vals[mid:]), 1)
                prior = sum(vals[:mid]) / max(mid, 1)
                pct_change = ((recent - prior) / max(prior, 1)) * 100
                result[term] = {
                    'recent_avg': round(recent, 1),
                    'prior_avg': round(prior, 1),
                    'pct_change': round(pct_change, 1),
                    'direction': '↑' if pct_change > 5 else '↓' if pct_change < -5 else '→',
                }
        return result
    except Exception as e:
        print(f"  pytrends interest error: {e}", file=sys.stderr)
        return {}


def is_relevant(text):
    text_lower = text.lower()
    return any(kw in text_lower for kw in RELEVANCE_KEYWORDS)


# ── Reddit helpers ────────────────────────────────────────────────────────────

def fetch_reddit_top(subreddit, limit=10, timeframe='week'):
    """Fetch top posts from a subreddit via Reddit's JSON API (no auth needed)."""
    url = f"https://www.reddit.com/r/{subreddit}/top.json?limit={limit}&t={timeframe}"
    headers = {'User-Agent': 'aiforlancaster-trends-agent/1.0'}
    try:
        import ssl, certifi
        ctx = ssl.create_default_context(cafile=certifi.where())
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            data = json.loads(resp.read().decode())
        posts = []
        for child in data.get('data', {}).get('children', []):
            p = child['data']
            posts.append({
                'title': p.get('title', ''),
                'score': p.get('score', 0),
                'comments': p.get('num_comments', 0),
                'url': 'https://reddit.com' + p.get('permalink', ''),
                'flair': p.get('link_flair_text', ''),
            })
        return posts
    except Exception as e:
        print(f"  Reddit error (r/{subreddit}): {e}", file=sys.stderr)
        return []


# ── Report builder ────────────────────────────────────────────────────────────

def build_report(trends_data, reddit_data, interest_data):
    now = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    lines = [
        f"LANCASTER / COLUMBUS DMA TRENDS — {now}",
        "=" * 50,
        "",
    ]

    # Interest over time
    if interest_data:
        lines.append("SEARCH MOMENTUM (Ohio, past 7 days vs prior 7 days)")
        lines.append("-" * 40)
        for term, d in sorted(interest_data.items(), key=lambda x: -abs(x[1]['pct_change'])):
            lines.append(f"  {d['direction']} {term:30s}  {d['pct_change']:+.0f}%  (index: {d['recent_avg']:.0f})")
        lines.append("")

    # Rising queries
    all_rising = []
    for seed, queries in trends_data.items():
        for q in queries:
            if is_relevant(q['query']):
                all_rising.append((q['query'], q['value'], seed))

    if all_rising:
        # Dedupe and sort by breakout value
        seen = set()
        deduped = []
        for query, value, seed in sorted(all_rising, key=lambda x: -x[1]):
            if query not in seen:
                seen.add(query)
                deduped.append((query, value, seed))

        lines.append("RISING QUERIES (Ohio, past 7 days, business-relevant)")
        lines.append("-" * 40)
        for query, value, seed in deduped[:15]:
            val_str = "Breakout" if value >= 5000 else f"+{value}%"
            lines.append(f"  {val_str:10s}  {query}  [via: {seed}]")
        lines.append("")
    else:
        lines.append("RISING QUERIES: no relevant results this week")
        lines.append("")

    # Reddit
    relevant_reddit = []
    for sub, posts in reddit_data.items():
        for p in posts:
            if is_relevant(p['title']) or sub in ('lancaster', 'AIBusiness'):
                relevant_reddit.append((sub, p))

    if relevant_reddit:
        lines.append("REDDIT SIGNAL (r/lancaster + r/smallbusiness + r/AIBusiness)")
        lines.append("-" * 40)
        for sub, p in sorted(relevant_reddit, key=lambda x: -x[1]['score'])[:10]:
            lines.append(f"  [{sub}] {p['title'][:80]}")
            lines.append(f"         ↑{p['score']}  {p['comments']} comments")
        lines.append("")

    lines.append("DATA LIMITATIONS")
    lines.append("-" * 40)
    lines.append("  • Google Trends resolves to Columbus DMA (not city-level)")
    lines.append("  • Rising = breakout or % increase vs prior period, not absolute volume")
    lines.append("  • Reddit r/lancaster is small — signal is sparse")
    lines.append("  • GSC data pending (wire up after domain verification)")
    lines.append("")

    return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--save', action='store_true', help='Save JSON to data/trends/')
    parser.add_argument('--quiet', action='store_true', help='Suppress stdout output')
    args = parser.parse_args()

    print("Fetching trends data...", file=sys.stderr)
    pt = get_pytrends_client()

    # 1. Interest over time for seed terms
    print("  Interest over time...", file=sys.stderr)
    interest_data = fetch_interest_over_time(pt, SEED_TERMS[:5])

    # 2. Rising queries per seed
    trends_data = {}
    for seed in RISING_SEEDS:
        print(f"  Rising queries: {seed}...", file=sys.stderr)
        trends_data[seed] = fetch_rising_queries(pt, seed)
        time.sleep(3)  # be polite to Google

    # 3. Reddit
    print("  Reddit...", file=sys.stderr)
    reddit_data = {}
    for sub in SUBREDDITS:
        reddit_data[sub] = fetch_reddit_top(sub)
        time.sleep(1)

    # Build report
    report = build_report(trends_data, reddit_data, interest_data)

    if not args.quiet:
        print(report)

    # Save JSON
    if args.save:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        out = {
            'date': today,
            'interest_over_time': interest_data,
            'rising_queries': trends_data,
            'reddit': reddit_data,
            'report': report,
        }
        out_path = DATA_DIR / f"{today}.json"
        out_path.write_text(json.dumps(out, indent=2))
        print(f"\nSaved: {out_path}", file=sys.stderr)

    return report


if __name__ == '__main__':
    main()

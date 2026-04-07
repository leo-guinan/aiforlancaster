#!/usr/bin/env python3
"""
aiforlancaster.com site builder.
Converts markdown guides to HTML pages using the dark theme.
Run from the local-ai-business directory.
"""

import os
import re
import json
import shutil
from pathlib import Path
from datetime import datetime

SITE_ROOT = Path(__file__).parent.parent
GUIDES_SRC = SITE_ROOT / "site" / "guides"
DEPLOY = SITE_ROOT / "deploy"
FATHOM_SNIPPET = '<script src="https://cdn.usefathom.com/script.js" data-site="CEYNPDYC" defer></script>'

NAV = '''<nav class="site-nav">
  <div class="container nav-inner">
    <a href="/" class="nav-brand">AI for Lancaster</a>
    <ul class="nav-links">
      <li><a href="/guides/">Guides</a></li>
      <li><a href="/prompts/">Prompts</a></li>
      <li><a href="/audit/">Free Audit</a></li>
      <li><a href="/#get-the-book" class="nav-cta">Get the Book</a></li>
    </ul>
  </div>
</nav>'''

SHARED_CSS = '''
/* =========================================
   AI for Main Street — Shared Styles
   ========================================= */
*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
html { scroll-behavior: smooth; font-size: 16px; }
body {
  background-color: #0a0a0a;
  color: #d4d4d4;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  line-height: 1.7;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
.container { max-width: 680px; margin: 0 auto; padding: 0 1.5rem; }
a { color: #8ab4f8; text-decoration: none; }
a:hover, a:focus { text-decoration: underline; }

/* ---- NAV ---- */
.site-nav {
  border-bottom: 1px solid #1a1a1a;
  padding: 1rem 0;
  position: sticky;
  top: 0;
  background: #0a0a0a;
  z-index: 100;
}
.nav-inner {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.nav-brand { color: #f0f0f0; font-weight: 700; font-size: 1rem; }
.nav-brand:hover { text-decoration: none; color: #fff; }
.nav-links { list-style: none; display: flex; gap: 1.5rem; align-items: center; }
.nav-links a { color: #888; font-size: 0.9rem; }
.nav-links a:hover { color: #f0f0f0; text-decoration: none; }
.nav-cta {
  background: #f0f0f0; color: #0a0a0a !important;
  padding: 0.4rem 1rem; border-radius: 4px; font-weight: 600;
}
.nav-cta:hover { background: #d4d4d4 !important; text-decoration: none !important; }

/* ---- HERO (homepage) ---- */
.hero {
  padding: 6rem 0 4rem;
  text-align: center;
  border-bottom: 1px solid #1a1a1a;
}
.hero h1 {
  font-size: 2.75rem;
  font-weight: 700;
  color: #f0f0f0;
  letter-spacing: -0.02em;
  margin-bottom: 0.5rem;
}
.hero .subtitle {
  font-size: 1.15rem;
  color: #999;
  margin-bottom: 1.5rem;
}
.hero .one-liner {
  font-size: 1.1rem;
  color: #b0b0b0;
  max-width: 500px;
  margin: 0 auto 2.5rem;
  font-style: italic;
}
.cta-button {
  display: inline-block;
  padding: 0.85rem 2rem;
  background-color: #f0f0f0;
  color: #0a0a0a;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 4px;
  text-decoration: none;
  transition: background-color 0.2s ease;
}
.cta-button:hover, .cta-button:focus {
  background-color: #d4d4d4;
  text-decoration: none;
}

/* ---- HOMEPAGE SECTIONS ---- */
.section-heading {
  font-size: 1.4rem;
  font-weight: 600;
  color: #e0e0e0;
  margin-bottom: 1.25rem;
  letter-spacing: -0.01em;
}
.problem { padding: 4rem 0; border-bottom: 1px solid #1a1a1a; }
.problem-text { font-size: 1.15rem; color: #b0b0b0; line-height: 1.8; }
.learn { padding: 4rem 0; border-bottom: 1px solid #1a1a1a; }
.learn-list { list-style: none; padding: 0; }
.learn-list li {
  padding: 0.75rem 0;
  padding-left: 1.5rem;
  position: relative;
  font-size: 1.05rem;
  color: #c8c8c8;
  border-bottom: 1px solid #141414;
}
.learn-list li:last-child { border-bottom: none; }
.learn-list li::before { content: "—"; position: absolute; left: 0; color: #555; }
.chapter-ref { color: #666; font-size: 0.9rem; }
.author { padding: 4rem 0; border-bottom: 1px solid #1a1a1a; }
.author-content { display: flex; gap: 2rem; align-items: flex-start; }
.author-photo {
  flex-shrink: 0; width: 120px; height: 120px;
  border-radius: 6px; object-fit: cover;
  display: block;
}
.author-bio p { color: #b0b0b0; font-size: 1rem; margin-bottom: 0.75rem; }
.author-email a { color: #8ab4f8; font-size: 0.95rem; }
.signup { padding: 4rem 0; border-bottom: 1px solid #1a1a1a; }
.signup-subtext { color: #888; font-size: 0.95rem; margin-bottom: 2rem; }
.signup-form { max-width: 420px; }
.form-group { margin-bottom: 1.25rem; }
.form-group label { display: block; font-size: 0.9rem; color: #999; margin-bottom: 0.4rem; }
.form-group .optional { color: #555; font-size: 0.8rem; }
.form-group .required { color: #c0392b; }
.form-group input {
  width: 100%; padding: 0.75rem 1rem;
  background-color: #141414; border: 1px solid #2a2a2a;
  border-radius: 4px; color: #e0e0e0; font-size: 1rem;
  font-family: inherit; transition: border-color 0.2s ease;
}
.form-group input::placeholder { color: #555; }
.form-group input:focus { outline: none; border-color: #555; }
.submit-button {
  display: inline-block; padding: 0.8rem 2rem;
  background-color: #f0f0f0; color: #0a0a0a;
  font-size: 1rem; font-weight: 600; border: none;
  border-radius: 4px; cursor: pointer; font-family: inherit;
  transition: background-color 0.2s ease;
}
.submit-button:hover, .submit-button:focus { background-color: #d4d4d4; }

/* ---- HOMEPAGE GUIDES SECTION ---- */
.guides-section { padding: 4rem 0; border-bottom: 1px solid #1a1a1a; }
.section-subheading { color: #888; font-size: 0.9rem; margin-top: -0.75rem; margin-bottom: 1.75rem; }
.guide-list { list-style: none; padding: 0; }
.guide-list li { padding: 0.65rem 0; border-bottom: 1px solid #141414; }
.guide-list li:last-child { border-bottom: none; }
.guide-list a {
  color: #8ab4f8;
  font-size: 1rem;
  text-decoration: none;
}
.guide-list a:hover { text-decoration: underline; color: #aecfff; }
.see-all {
  display: inline-block; margin-top: 1.25rem;
  color: #8ab4f8; font-size: 0.9rem;
}
.see-all:hover { text-decoration: underline; }

/* ---- GUIDE PAGE ---- */
.guide-header { padding: 4rem 0 2rem; border-bottom: 1px solid #1a1a1a; }
.guide-header h1 {
  font-size: 2rem; font-weight: 700; color: #f0f0f0;
  letter-spacing: -0.02em; margin-bottom: 0.75rem;
}
.guide-meta { color: #555; font-size: 0.85rem; }
.guide-body { padding: 3rem 0; }
/* Suppress the redundant H1 that markdown renders from the # title line */
.guide-body > h1:first-child { display: none; }
.guide-body h2 {
  font-size: 1.3rem; font-weight: 600; color: #e0e0e0;
  margin: 2.5rem 0 1rem; letter-spacing: -0.01em;
}
.guide-body h3 { font-size: 1.1rem; font-weight: 600; color: #d0d0d0; margin: 2rem 0 0.75rem; }
.guide-body h4 { font-size: 1rem; font-weight: 600; color: #c0c0c0; margin: 1.5rem 0 0.5rem; }
.guide-body p { color: #b0b0b0; margin-bottom: 1.25rem; }
.guide-body ul, .guide-body ol { padding-left: 1.5rem; margin-bottom: 1.25rem; }
.guide-body li { color: #b0b0b0; margin-bottom: 0.5rem; }
.guide-body strong { color: #d4d4d4; }
.guide-body a { color: #8ab4f8; }
.guide-body a:hover { text-decoration: underline; color: #aecfff; }
.guide-body blockquote {
  border-left: 3px solid #2a2a2a; padding-left: 1.25rem;
  margin: 1.5rem 0; color: #888; font-style: italic;
}
.guide-body hr { border: none; border-top: 1px solid #1a1a1a; margin: 2.5rem 0; }
.guide-cta {
  background: #111; border: 1px solid #222; border-radius: 6px;
  padding: 2rem; margin: 3rem 0; text-align: center;
}
.guide-cta p { color: #999; margin-bottom: 1rem; }
.guide-cta a {
  display: inline-block; padding: 0.75rem 1.75rem;
  background: #f0f0f0; color: #0a0a0a; font-weight: 600;
  border-radius: 4px; font-size: 0.95rem; text-decoration: none;
}
.guide-cta a:hover { background: #d4d4d4; }
.breadcrumb { color: #555; font-size: 0.85rem; margin-bottom: 1.5rem; }
.breadcrumb a { color: #666; }
.breadcrumb a:hover { color: #8ab4f8; }

/* ---- GUIDES INDEX ---- */
.guides-grid { display: flex; flex-direction: column; gap: 0; }
.guide-card { padding: 1.5rem 0; border-bottom: 1px solid #1a1a1a; }
.guide-card:last-child { border-bottom: none; }
.guide-card h3 { font-size: 1.05rem; font-weight: 600; margin-bottom: 0.4rem; }
.guide-card h3 a { color: #8ab4f8; text-decoration: none; }
.guide-card h3 a:hover { text-decoration: underline; color: #aecfff; }
.guide-card p { color: #777; font-size: 0.9rem; margin: 0; }
.page-header { padding: 4rem 0 2rem; border-bottom: 1px solid #1a1a1a; }
.page-header h1 { font-size: 2rem; font-weight: 700; color: #f0f0f0; margin-bottom: 0.5rem; letter-spacing: -0.02em; }
.page-header p { color: #888; }

/* ---- FOOTER ---- */
.site-footer { padding: 3rem 0; text-align: center; border-top: 1px solid #1a1a1a; margin-top: 4rem; }
.site-footer p { color: #555; font-size: 0.85rem; margin-bottom: 0.35rem; }
.site-footer a { color: #666; font-size: 0.85rem; }
.site-footer a:hover { color: #8ab4f8; }
.footer-links { display: flex; gap: 1.5rem; justify-content: center; margin-bottom: 1rem; }
.amazon-link { color: #666; font-size: 0.85rem; }
.amazon-link:hover { color: #8ab4f8; }

/* ---- RESPONSIVE ---- */
@media (max-width: 600px) {
  .nav-links { display: none; }
  .hero { padding: 4rem 0 3rem; }
  .hero h1 { font-size: 2rem; }
  .hero .subtitle { font-size: 1rem; }
  .hero .one-liner { font-size: 1rem; }
  .problem, .learn, .author, .signup { padding: 3rem 0; }
  .author-content { flex-direction: column; align-items: center; text-align: center; }
  .author-photo { width: 100px; height: 100px; }
  .signup-form { max-width: 100%; }
  .submit-button { width: 100%; }
  .guide-header h1 { font-size: 1.5rem; }
  .guide-body h2 { font-size: 1.15rem; }
}
'''

FOOTER_HTML = '''<footer class="site-footer">
  <div class="container">
    <div class="footer-links">
      <a href="/guides/">Guides</a>
      <a href="/prompts/">Prompts</a>
      <a href="/audit/">Free Audit</a>
      <a href="mailto:leo@aiforlancaster.com">Contact</a>
    </div>
    <p>&copy; 2026 Leo Guinan / MetaSPN &mdash; Lancaster, Ohio</p>
    <p style="margin-top:0.5rem"><a href="/">AI for Lancaster</a></p>
  </div>
</footer>'''


def parse_frontmatter(text):
    """Extract YAML-ish frontmatter and body from markdown.
    Handles both inline values and YAML list syntax for keywords."""
    if not text.startswith('---'):
        return {}, text
    parts = text.split('---', 2)
    if len(parts) < 3:
        return {}, text
    meta = {}
    current_list_key = None
    for line in parts[1].strip().splitlines():
        # YAML list item under a previous key
        if current_list_key and re.match(r'^\s+-\s+', line):
            item = re.sub(r'^\s+-\s+', '', line).strip().strip('"')
            if isinstance(meta[current_list_key], list):
                meta[current_list_key].append(item)
            continue
        current_list_key = None
        if ':' in line:
            k, _, v = line.partition(':')
            k = k.strip()
            v = v.strip().strip('"')
            if v == '':
                # Value is a YAML list on following lines
                meta[k] = []
                current_list_key = k
            else:
                meta[k] = v
    # Collapse list keywords to comma string for meta tag
    if 'keywords' in meta and isinstance(meta['keywords'], list):
        meta['keywords'] = ', '.join(meta['keywords'])
    return meta, parts[2].strip()


def md_to_html(text):
    """Minimal markdown-to-HTML converter sufficient for guide content."""
    lines = text.split('\n')
    html = []
    in_ul = False
    in_ol = False

    def close_lists():
        nonlocal in_ul, in_ol
        if in_ul:
            html.append('</ul>')
            in_ul = False
        if in_ol:
            html.append('</ol>')
            in_ol = False

    for line in lines:
        # Headings
        if line.startswith('#### '):
            close_lists()
            html.append(f'<h4>{inline_md(line[5:])}</h4>')
        elif line.startswith('### '):
            close_lists()
            html.append(f'<h3>{inline_md(line[4:])}</h3>')
        elif line.startswith('## '):
            close_lists()
            html.append(f'<h2>{inline_md(line[3:])}</h2>')
        elif line.startswith('# '):
            close_lists()
            html.append(f'<h1>{inline_md(line[2:])}</h1>')
        # Horizontal rule
        elif re.match(r'^---+$', line.strip()):
            close_lists()
            html.append('<hr>')
        # Unordered list
        elif re.match(r'^[-*] ', line):
            if not in_ul:
                close_lists()
                html.append('<ul>')
                in_ul = True
            html.append(f'<li>{inline_md(line[2:])}</li>')
        # Ordered list
        elif re.match(r'^\d+\. ', line):
            if not in_ol:
                close_lists()
                html.append('<ol>')
                in_ol = True
            clean = re.sub(r'^\d+\. ', '', line)
            html.append(f'<li>{inline_md(clean)}</li>')
        # Blockquote
        elif line.startswith('> '):
            close_lists()
            html.append(f'<blockquote><p>{inline_md(line[2:])}</p></blockquote>')
        # Empty line
        elif line.strip() == '':
            close_lists()
        # Paragraph
        else:
            close_lists()
            html.append(f'<p>{inline_md(line)}</p>')

    close_lists()
    return '\n'.join(html)


def inline_md(text):
    """Handle inline markdown: bold, italic, code, links."""
    # Bold+italic
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', text)
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # Inline code
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    # Links
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    return text


def build_guide_html(meta, body_html, slug, all_guides):
    title = meta.get('title', 'AI Guide')
    description = meta.get('description', '')
    date_str = meta.get('date', '2026-01-01')

    # Related guides (all except self)
    related = [g for g in all_guides if g['slug'] != slug][:3]
    related_html = ''
    if related:
        items = ''.join(f'<li><a href="/guides/{g["slug"]}/">{g["title"]}</a></li>' for g in related)
        related_html = f'<div style="margin-top:3rem;padding-top:2rem;border-top:1px solid #1a1a1a"><p style="color:#666;font-size:0.85rem;margin-bottom:0.75rem">MORE GUIDES</p><ul class="guide-list">{items}</ul></div>'

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{description}">
  <meta name="author" content="Leo Guinan">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:type" content="article">
  <title>{title} — AI for Lancaster</title>
  <link rel="icon" href="/favicon.ico" type="image/x-icon">
  <link rel="stylesheet" href="/style.css">
  {FATHOM_SNIPPET}
</head>
<body>
{NAV}
<main>
  <div class="container">
    <div class="guide-header">
      <p class="breadcrumb"><a href="/">Home</a> &rsaquo; <a href="/guides/">Guides</a> &rsaquo; {title}</p>
      <h1>{title}</h1>
      <p class="guide-meta">By Leo Guinan &mdash; Lancaster, Ohio &mdash; {date_str}</p>
    </div>
    <div class="guide-body">
      {body_html}
      <div class="guide-cta">
        <p>Want the full playbook? The book covers all of this in depth &mdash; and it&rsquo;s free.</p>
        <a href="/#get-the-book">Get the Free PDF</a>
      </div>
      {related_html}
    </div>
  </div>
</main>
{FOOTER_HTML}
</body>
</html>'''


def build_guides_index(all_guides):
    items = ''
    for g in sorted(all_guides, key=lambda x: x.get('date', ''), reverse=True):
        items += f'''<div class="guide-card">
  <h3><a href="/guides/{g["slug"]}/">{g["title"]}</a></h3>
  <p>{g["description"]}</p>
</div>
'''
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="No-hype AI guides for small business owners. What works, what costs what, and what to skip. Written by Leo Guinan in Lancaster, Ohio.">
  <title>AI Guides for Small Business — AI for Lancaster</title>
  <link rel="icon" href="/favicon.ico" type="image/x-icon">
  <link rel="stylesheet" href="/style.css">
  {FATHOM_SNIPPET}
</head>
<body>
{NAV}
<main>
  <div class="container">
    <div class="page-header">
      <h1>Guides</h1>
      <p>What AI actually does for small businesses. No hype, no affiliates, no sponsors.</p>
    </div>
    <div class="guides-grid">
      {items}
    </div>
  </div>
</main>
{FOOTER_HTML}
</body>
</html>'''


def build_homepage(all_guides):
    """Rebuild index.html with nav, Fathom, and guides section injected."""
    top_guides = sorted(all_guides, key=lambda x: x.get('date', ''), reverse=True)[:6]
    guide_items = ''.join(
        f'<li><a href="/guides/{g["slug"]}/">{g["title"]}</a></li>'
        for g in top_guides
    )
    guides_section = f'''
    <!-- Guides -->
    <section class="guides-section" aria-labelledby="guides-heading">
      <div class="container">
        <h2 id="guides-heading" class="section-heading">Free Guides</h2>
        <p class="section-subheading">Plain English. Real numbers. No sales pitch.</p>
        <ul class="guide-list">
          {guide_items}
        </ul>
        <a href="/guides/" class="see-all">See all guides &rarr;</a>
      </div>
    </section>'''

    # Always read from the canonical template, never from the already-built output
    template_path = SITE_ROOT / 'landing-page' / 'index.html'
    src = template_path.read_text()

    # Replace stylesheet ref + add Fathom
    src = src.replace(
        '<link rel="stylesheet" href="style.css">',
        f'<link rel="stylesheet" href="/style.css">\n  {FATHOM_SNIPPET}'
    )

    # Inject nav once, right after <body>
    src = src.replace('<body>\n', f'<body>\n{NAV}\n')

    # Inject guides section before email capture
    src = src.replace(
        '    <!-- Email Capture Form -->',
        guides_section + '\n\n    <!-- Email Capture Form -->'
    )

    # Update footer
    old_footer = '''  <!-- Footer -->
  <footer class="site-footer">
    <div class="container">
      <p>&copy; 2026 Leo Guinan / MetaSPN</p>
      <p>Lancaster, Ohio</p>
      <p><a href="#" class="amazon-link">Also available on Amazon</a></p>
    </div>
  </footer>'''
    src = src.replace(old_footer, FOOTER_HTML)

    return src


def patch_existing_page(path):
    """Add Fathom + nav + stylesheet link update to an existing page."""
    src = path.read_text()
    if 'usefathom' in src:
        return src  # already patched
    # Add fathom before </head>
    src = src.replace('</head>', f'  {FATHOM_SNIPPET}\n</head>')
    # Fix absolute stylesheet path if needed
    src = src.replace('href="style.css"', 'href="/style.css"')
    src = src.replace("href='style.css'", "href='/style.css'")
    # Inject nav after <body> tag (if not already there)
    if 'site-nav' not in src:
        src = src.replace('<body>\n', f'<body>\n{NAV}\n')
        src = src.replace('<body>', f'<body>\n{NAV}')
    return src


def make_sitemap(all_guides):
    """Generate sitemap.xml for the full site."""
    today = datetime.now().strftime('%Y-%m-%d')
    urls = []

    def url(loc, priority, changefreq):
        return f'''  <url>
    <loc>{loc}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>'''

    urls.append(url('https://www.aiforlancaster.com/', '1.0', 'weekly'))
    urls.append(url('https://www.aiforlancaster.com/guides/', '0.9', 'daily'))
    urls.append(url('https://www.aiforlancaster.com/audit/', '0.8', 'monthly'))
    urls.append(url('https://www.aiforlancaster.com/prompts/', '0.8', 'monthly'))
    urls.append(url('https://www.aiforlancaster.com/call/', '0.7', 'monthly'))

    for g in sorted(all_guides, key=lambda x: x.get('date', ''), reverse=True):
        urls.append(url(
            f"https://www.aiforlancaster.com/guides/{g['slug']}/",
            '0.8', 'monthly'
        ))

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>'''


def build_link_index(all_guides):
    """
    Build an index of specific anchor phrases -> guide URL.
    Only uses the distinctive noun phrase from each guide title,
    not generic words like "small business" or "for business".
    Max 1 link per target guide per page, max 4 auto-links per page total.
    """
    # Hand-tuned distinctive phrases per guide slug.
    # These are phrases that are specific enough to link without false matches.
    ANCHOR_PHRASES = {
        'ai-voice-agents-small-business':       ['voice agent', 'voice agents', 'AI voice agent'],
        'ai-automation-small-business':          ['Zapier', 'Make.com', 'workflow automation', 'automate your'],
        'ai-customer-service-small-business':    ['AI customer service', 'customer service chatbot'],
        'ai-marketing-small-business':           ['AI marketing', 'marketing automation'],
        'ai-social-media-small-business':        ['social media content', 'batch.*content', 'content batching'],
        'ai-email-tools-small-business':         ['email automation', 'AI email', 'email drafting'],
        'ai-for-accounting-bookkeeping':         ['QuickBooks', 'bookkeeping', 'accounting software'],
        'ai-for-restaurants':                    ['restaurant', 'reservation', 'menu optimization'],
        'ai-for-retail-stores':                  ['retail', 'inventory management', 'product description'],
        'ai-for-contractors':                    ['contractor', 'estimate', 'job site'],
        'ai-for-law-offices':                    ['law office', 'legal AI', 'client intake'],
        'ai-for-medical-offices':                ['HIPAA', 'medical office', 'dental office', 'appointment reminder'],
        'ai-for-real-estate-agents':             ['real estate', 'listing description', 'lead nurture'],
        'ai-for-home-services':                  ['HVAC', 'plumbing', 'home service'],
        'ai-for-salons-spas':                    ['salon', 'spa', 'rebooking'],
        'ai-for-nonprofits':                     ['nonprofit', 'grant writing'],
        'ai-for-auto-shops':                     ['auto shop', 'repair shop', 'mechanic'],
        'ai-scheduling-tools':                   ['Calendly', 'Acuity', 'online booking', 'appointment booking'],
        'best-ai-phone-answering-service':       ['phone answering', 'AI receptionist', 'answer.*phone'],
        'chatgpt-vs-claude-vs-gemini-small-business': ['ChatGPT vs', 'Claude vs', 'which AI tool'],
        'how-to-use-chatgpt-for-business':       ['prompt framework', 'how to use ChatGPT', 'custom instruction'],
        'ai-tools-comparison-2025':              ['AI tools comparison', 'compare AI tools'],
        'ai-tools-free-tier-guide':              ['free tier', 'free version of', 'without paying'],
        'ai-content-marketing-local-business':   ['local SEO', 'rank.*locally', 'Google Business Profile'],
        'what-is-ai-small-business':             ['what AI actually is', 'AI explained', 'how AI works'],
        'hire-ai-consultant-without-getting-burned': ['hire.*consultant', 'red flag', 'AI consultant'],
        'how-to-audit-business-for-ai':          ['AI audit', 'audit your business', 'find AI opportunities'],
        'ai-for-insurance-agents':               ['insurance agent', 'policy document'],
        'ai-for-gyms-fitness':                   ['gym', 'fitness studio', 'personal trainer'],
        'ai-for-childcare':                      ['childcare', 'daycare'],
        'ai-for-pet-services':                   ['pet service', 'veterinary', 'grooming'],
    }
    # Build slug -> [(regex_pattern, url), ...]
    index = {}
    for g in all_guides:
        slug = g['slug']
        url = f'/guides/{slug}/'
        phrases = ANCHOR_PHRASES.get(slug, [])
        patterns = []
        for phrase in phrases:
            # Build case-insensitive regex
            try:
                pat = re.compile(r'\b(' + phrase + r')\b', re.IGNORECASE)
                patterns.append((pat, url))
            except re.error:
                pass
        if patterns:
            index[slug] = patterns
    return index


def autolink_body(html_body, current_slug, link_index, max_links=4):
    """
    Insert internal links into guide body HTML.
    Rules:
    - Skip the current guide's own patterns
    - Max 1 link per target guide
    - Max max_links total auto-links per page
    - Never link inside existing <a> tags
    - Never link inside <h1>/<h2>/<h3> tags
    - First occurrence only
    """
    # Pre-populate already-linked slugs from existing <a href="/guides/..."> in the HTML
    linked_slugs = set(re.findall(r'href="/guides/([^/]+)/', html_body))
    link_count = [0]

    def replacer(match, url):
        if link_count[0] >= max_links:
            return match.group(0)
        link_count[0] += 1
        return f'<a href="{url}">{match.group(0)}</a>'

    # Split on tags we don't want to touch, process text nodes only
    # Strategy: split HTML into segments, only process text outside <a>, <h1-3> tags
    def process_segment(seg, slug, pat, url):
        """Apply one pattern to one text segment, first occurrence only."""
        return pat.sub(lambda m: replacer(m, url), seg, count=1)

    # Parse out tag vs text segments
    TAG_RE = re.compile(r'(<[^>]+>)')
    segments = TAG_RE.split(html_body)

    in_anchor = False
    in_heading = False
    result = []

    for seg in segments:
        if seg.startswith('<'):
            tag_lower = seg.lower()
            if re.match(r'<a[\s>]', tag_lower):
                in_anchor = True
            elif tag_lower.startswith('</a'):
                in_anchor = False
            elif re.match(r'<h[123][\s>]', tag_lower):
                in_heading = True
            elif re.match(r'</h[123]', tag_lower):
                in_heading = False
            result.append(seg)
        else:
            if in_anchor or in_heading or link_count[0] >= max_links:
                result.append(seg)
                continue
            # Try each guide's patterns
            current_seg = seg
            for slug, patterns in link_index.items():
                if slug == current_slug:
                    continue
                if slug in linked_slugs:
                    continue
                if link_count[0] >= max_links:
                    break
                for pat, url in patterns:
                    m = pat.search(current_seg)
                    if m:
                        current_seg = pat.sub(
                            lambda match, u=url: replacer(match, u),
                            current_seg, count=1
                        )
                        linked_slugs.add(slug)
                        break
            result.append(current_seg)

    return ''.join(result)


def main():
    # 1. Write shared stylesheet
    (DEPLOY / 'style.css').write_text(SHARED_CSS)
    print('Wrote style.css')

    # 2. Parse all guide markdown files
    all_guides = []
    guide_dir = GUIDES_SRC
    if guide_dir.exists():
        for md_file in sorted(guide_dir.glob('*.md')):
            src = md_file.read_text()
            meta, body = parse_frontmatter(src)
            slug = md_file.stem
            all_guides.append({
                'slug': slug,
                'title': meta.get('title', slug.replace('-', ' ').title()),
                'description': meta.get('description', ''),
                'date': meta.get('date', '2026-01-01'),
                'meta': meta,
                'body': body,
            })

    print(f'Found {len(all_guides)} guide files')

    # 3. Build auto-link index (specific phrases -> guide URLs)
    link_index = build_link_index(all_guides)
    print(f'Built link index ({len(link_index)} guides with anchor phrases)')

    # 4. Build each guide HTML page
    guides_deploy = DEPLOY / 'guides'
    guides_deploy.mkdir(exist_ok=True)
    total_links = 0
    for g in all_guides:
        body_html = md_to_html(g['body'])
        body_html = autolink_body(body_html, g['slug'], link_index)
        # Count links inserted (rough)
        total_links += body_html.count('href="/guides/')
        html = build_guide_html(g['meta'], body_html, g['slug'], all_guides)
        out_dir = guides_deploy / g['slug']
        out_dir.mkdir(exist_ok=True)
        (out_dir / 'index.html').write_text(html)
        print(f'  Built /guides/{g["slug"]}/')
    print(f'  ({total_links} internal links inserted across all guides)')

    # 5. Build guides index
    (guides_deploy / 'index.html').write_text(build_guides_index(all_guides))
    print('Built /guides/')

    # 6. Rebuild homepage with guides section + nav + Fathom
    homepage = build_homepage(all_guides)
    (DEPLOY / 'index.html').write_text(homepage)
    print('Rebuilt index.html')

    # 7. Patch existing pages (audit, call, prompts, 404)
    for p in [DEPLOY / 'audit' / 'index.html',
               DEPLOY / 'call' / 'index.html',
               DEPLOY / 'prompts' / 'index.html',
               DEPLOY / '404.html']:
        if p.exists():
            p.write_text(patch_existing_page(p))
            print(f'  Patched {p.relative_to(DEPLOY)}')

    # 8. Generate and write sitemap.xml
    sitemap = make_sitemap(all_guides)
    (DEPLOY / 'sitemap.xml').write_text(sitemap)
    print(f'Wrote sitemap.xml ({len(all_guides) + 5} URLs)')

    # 9. Write a manifest of all guides (used by cron)
    manifest = [{'slug': g['slug'], 'title': g['title'], 'date': g['date']} for g in all_guides]
    (SITE_ROOT / 'site' / 'guides-manifest.json').write_text(json.dumps(manifest, indent=2))
    print(f'Wrote guides-manifest.json ({len(manifest)} guides)')
    print('\nBuild complete.')


if __name__ == '__main__':
    main()

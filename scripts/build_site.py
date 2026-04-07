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
}
.container { max-width: 680px; margin: 0 auto; padding: 0 1.5rem; }
a { color: #8ab4f8; text-decoration: none; }
a:hover, a:focus { text-decoration: underline; }

/* Nav */
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
.nav-links a { color: #999; font-size: 0.9rem; }
.nav-links a:hover { color: #f0f0f0; text-decoration: none; }
.nav-cta {
  background: #f0f0f0; color: #0a0a0a !important;
  padding: 0.4rem 1rem; border-radius: 4px; font-weight: 600;
}
.nav-cta:hover { background: #d4d4d4 !important; }

/* Footer */
.site-footer { padding: 3rem 0; text-align: center; border-top: 1px solid #1a1a1a; margin-top: 4rem; }
.site-footer p { color: #555; font-size: 0.85rem; margin-bottom: 0.35rem; }
.site-footer a { color: #666; font-size: 0.85rem; }
.site-footer a:hover { color: #8ab4f8; }
.footer-links { display: flex; gap: 1.5rem; justify-content: center; margin-bottom: 1rem; }

/* Guide page styles */
.guide-header { padding: 4rem 0 2rem; border-bottom: 1px solid #1a1a1a; }
.guide-header h1 { font-size: 2rem; font-weight: 700; color: #f0f0f0; letter-spacing: -0.02em; margin-bottom: 0.75rem; }
.guide-meta { color: #666; font-size: 0.85rem; }
.guide-body { padding: 3rem 0; }
.guide-body h2 { font-size: 1.3rem; font-weight: 600; color: #e0e0e0; margin: 2.5rem 0 1rem; letter-spacing: -0.01em; }
.guide-body h3 { font-size: 1.1rem; font-weight: 600; color: #d0d0d0; margin: 2rem 0 0.75rem; }
.guide-body p { color: #b0b0b0; margin-bottom: 1.25rem; }
.guide-body ul, .guide-body ol { padding-left: 1.5rem; margin-bottom: 1.25rem; }
.guide-body li { color: #b0b0b0; margin-bottom: 0.5rem; }
.guide-body strong { color: #d4d4d4; }
.guide-body a { color: #8ab4f8; }
.guide-body blockquote {
  border-left: 3px solid #333; padding-left: 1.25rem;
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
  border-radius: 4px; font-size: 0.95rem;
}
.guide-cta a:hover { background: #d4d4d4; text-decoration: none; }
.breadcrumb { color: #555; font-size: 0.85rem; margin-bottom: 1.5rem; }
.breadcrumb a { color: #666; }
.breadcrumb a:hover { color: #8ab4f8; }

/* Guides index */
.guides-grid { display: flex; flex-direction: column; gap: 0; }
.guide-card {
  padding: 1.5rem 0;
  border-bottom: 1px solid #1a1a1a;
}
.guide-card:last-child { border-bottom: none; }
.guide-card h3 { font-size: 1.05rem; font-weight: 600; color: #e0e0e0; margin-bottom: 0.4rem; }
.guide-card h3 a { color: #e0e0e0; }
.guide-card h3 a:hover { color: #8ab4f8; text-decoration: none; }
.guide-card p { color: #888; font-size: 0.9rem; margin: 0; }
.guide-card .guide-date { color: #555; font-size: 0.8rem; margin-top: 0.4rem; }
.page-header { padding: 4rem 0 2rem; border-bottom: 1px solid #1a1a1a; }
.page-header h1 { font-size: 2rem; font-weight: 700; color: #f0f0f0; margin-bottom: 0.5rem; }
.page-header p { color: #888; }

/* Homepage guides section */
.guides-section { padding: 4rem 0; border-bottom: 1px solid #1a1a1a; }
.section-heading { font-size: 1.4rem; font-weight: 600; color: #e0e0e0; margin-bottom: 1.5rem; }
.section-subheading { color: #888; font-size: 0.9rem; margin-top: -1rem; margin-bottom: 1.5rem; }
.guide-list { list-style: none; padding: 0; }
.guide-list li { padding: 0.65rem 0; border-bottom: 1px solid #141414; }
.guide-list li:last-child { border-bottom: none; }
.guide-list a { color: #c8c8c8; font-size: 1rem; }
.guide-list a:hover { color: #8ab4f8; }
.see-all { display: inline-block; margin-top: 1.25rem; color: #666; font-size: 0.9rem; }
.see-all:hover { color: #8ab4f8; }

@media (max-width: 600px) {
  .nav-links { display: none; }
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
    """Extract YAML-ish frontmatter and body from markdown."""
    if not text.startswith('---'):
        return {}, text
    parts = text.split('---', 2)
    if len(parts) < 3:
        return {}, text
    meta = {}
    for line in parts[1].strip().splitlines():
        if ':' in line:
            k, _, v = line.partition(':')
            meta[k.strip()] = v.strip().strip('"')
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

    # 3. Build each guide HTML page
    guides_deploy = DEPLOY / 'guides'
    guides_deploy.mkdir(exist_ok=True)
    for g in all_guides:
        body_html = md_to_html(g['body'])
        html = build_guide_html(g['meta'], body_html, g['slug'], all_guides)
        out_dir = guides_deploy / g['slug']
        out_dir.mkdir(exist_ok=True)
        (out_dir / 'index.html').write_text(html)
        print(f'  Built /guides/{g["slug"]}/')

    # 4. Build guides index
    (guides_deploy / 'index.html').write_text(build_guides_index(all_guides))
    print('Built /guides/')

    # 5. Rebuild homepage with guides section + nav + Fathom
    homepage = build_homepage(all_guides)
    (DEPLOY / 'index.html').write_text(homepage)
    print('Rebuilt index.html')

    # 6. Patch existing pages (audit, call, prompts, 404)
    for p in [DEPLOY / 'audit' / 'index.html',
               DEPLOY / 'call' / 'index.html',
               DEPLOY / 'prompts' / 'index.html',
               DEPLOY / '404.html']:
        if p.exists():
            p.write_text(patch_existing_page(p))
            print(f'  Patched {p.relative_to(DEPLOY)}')

    # 7. Write a manifest of all guides (used by cron)
    manifest = [{'slug': g['slug'], 'title': g['title'], 'date': g['date']} for g in all_guides]
    (SITE_ROOT / 'site' / 'guides-manifest.json').write_text(json.dumps(manifest, indent=2))
    print(f'Wrote guides-manifest.json ({len(manifest)} guides)')
    print('\nBuild complete.')


if __name__ == '__main__':
    main()

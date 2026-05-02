#!/usr/bin/env python3
"""
Build and deploy bodega.aiforlancaster.com — Bottega Bodega membership site.
Retro RPG themed static site + backend Flask API.
"""

import os
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent.parent
DEPLOY = ROOT / 'deploy' / 'bodega'
LANDING = ROOT / 'landing-page'
ICONS = LANDING / 'icons'

# Ensure deploy dirs
(DEPLOY / 'icons').mkdir(parents=True, exist_ok=True)

def copy_assets():
    """Copy bodega landing page + icons to deploy folder."""
    import shutil
    
    # Copy index.html
    shutil.copy(LANDING / 'bodega-index.html', DEPLOY / 'index.html')
    print(f"✓ Copied bodega-index.html → {DEPLOY}/index.html")
    
    # Copy CSS
    shutil.copy(LANDING / 'bodega-style.css', DEPLOY / 'bodega-style.css')
    print(f"✓ Copied bodega-style.css → {DEPLOY}/bodega-style.css")
    
    # Copy icons
    for icon in ICONS.glob('*.png'):
        dest = DEPLOY / 'icons' / icon.name
        shutil.copy(icon, dest)
        print(f"✓ Copied icon {icon.name}")
    # Also copy to top-level deploy/icons for root-relative /icons/ URL
    ROOT_ICONS = ROOT / 'deploy' / 'icons'
    ROOT_ICONS.mkdir(parents=True, exist_ok=True)
    for icon in ICONS.glob('*.png'):
        root_dest = ROOT_ICONS / icon.name
        shutil.copy(icon, root_dest)
        print(f"✓ Synced icon to deploy root: {icon.name}")
    
    # Copy favicon fallback (optional: generate one later)
    # TODO: generate favicon.ico from one of the icons

def update_css_references():
    """Patch index.html to reference correct stylesheet path."""
    html = (DEPLOY / 'index.html').read_text()
    html = html.replace('href="/bodega-style.css"', 'href="bodega-style.css"')
    (DEPLOY / 'index.html').write_text(html)
    print("✓ Patched stylesheet reference")

def run_checks():
    """Verify deploy output is sane."""
    required = ['index.html', 'bodega-style.css']
    for f in required:
        if not (DEPLOY / f).exists():
            print(f"✗ MISSING: {f}")
            return False
    icon_count = len(list((DEPLOY / 'icons').glob('*.png')))
    if icon_count < 2:
        print(f"✗ MISSING ICONS: only {icon_count} found")
        return False
    print(f"✓ All checks passed ({icon_count} icons, pages present)")
    return True

def deploy_to_cloudflare():
    """Deploy deploy/bodega/ as a separate Cloudflare Pages project."""
    print("=== Deploy to Cloudflare Pages ===")
    print("Manual steps (requires wrangler config for second project):")
    print(f"  1. cd {ROOT}")
    print(f"  2. npx wrangler pages deploy ./deploy/bodega --project-name=bodega-aiforlancaster")
    print("  3. In Cloudflare dashboard: add custom domain bodega.aiforlancaster.com")
    print("     pointing to the bodega-aiforlancaster.pages.dev project")

def main():
    print("=== Bodega Site Build ===")
    copy_assets()
    update_css_references()
    if run_checks():
        print("✓ Build successful. Deploy directory: deploy/bodega/")
        deploy_to_cloudflare()
    else:
        print("✗ Build FAILED — check errors above")
        sys.exit(1)

if __name__ == "__main__":
    main()

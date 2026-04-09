#!/bin/bash
# Deploy aiforlancaster.com to Cloudflare Pages
# Run from ~/clawd/local-ai-business

cd "$(dirname "$0")/.."
npx wrangler pages deploy deploy --project-name=aiforlancaster 2>&1 | tail -5

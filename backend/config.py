"""
Bodega backend configuration.
Environment variables required:
  - STRIPE_SECRET_KEY: sk_live_...
  - STRIPE_PUBLISHABLE_KEY: pk_live_...
  - STRIPE_WEBHOOK_SECRET: whsec_...
  - ADMIN_PASSWORD: simple string (for admin area)
  - RESEND_API_KEY: for transactional email
  - DATABASE_URL: sqlite:///data/bodega.db (default)
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'bodega-secret-key-change-in-prod')
    DATABASE = os.getenv('DATABASE_URL', f"sqlite:///{BASE_DIR / 'data' / 'bodega.db'}")
    STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
    STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')
    STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'bodega-admin')
    RESEND_API_KEY = os.getenv('RESEND_API_KEY')
    MARVIN_AGENT_PATH = os.getenv('MARVIN_AGENT_PATH', '/Users/leoguinan/.hermes/agents/marvin')
    
    # Pricing (in cents) — used as fallback if price_id not supplied
    PRICE_MALLRAT = 2500   # $25.00
    PRICE_DINING = 100000 # $1,000.00
    PRICE_MARVIN = 100    # $1.00 minimum (PWYW; actual amount set by Stripe Price)
    
    # URLs
    BODEGA_URL = os.getenv('BODEGA_URL', 'https://bodega.aiforlancaster.com')
    ADMIN_URL = f"{BODEGA_URL}/admin"
    FRONTEND_URL = os.getenv('FRONTEND_URL', BODEGA_URL)  # CORS origin
    BOTTEGA_URL = os.getenv('BOTTEGA_URL', 'https://api.bodega.aiforlancaster.com')  # API subdomain


#!/bin/bash
# Bottega Bodega Backend Setup — run on arc-vps
# This script sets up the Flask backend, nginx, and systemd service.

set -e

echo "=== Bottega Bodega Backend Setup ==="
cd /opt

# 1. Create backend directory
echo "Creating directory structure..."
mkdir -p bodega-backend/{templates,static/{content,wall,ballads,events},data}

# 2. Copy files from local source
# You need to upload the 'backend/' folder from ~/clawd/local-ai-business/
# scp -r ~/clawd/local-ai-business/backend/* arc-vps:/opt/bodega-backend/

# 3. Create Python virtual environment
echo "Setting up Python venv..."
python3 -m venv /opt/bodega-backend/venv
source /opt/bodega-backend/venv/bin/activate

# 4. Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r /opt/bodega-backend/requirements.txt

# 5. Initialize database
echo "Initializing database..."
source /opt/bodega-backend/venv/bin/activate
python -c "from models import init_db; init_db()"
echo "Database created at /opt/bodega-backend/data/bodega.db"

# 6. Set up environment file
echo "Setting up .env..."
cp /opt/bodega-backend/.env.example /opt/bodega-backend/.env
echo "⚠️  EDIT /opt/bodega-backend/.env with your real API keys before starting!"

# 7. Install systemd service
echo "Installing systemd service..."
sudo cp /tmp/bodega.service /etc/systemd/system/bodega-backend.service
sudo systemctl daemon-reload
sudo systemctl enable bodega-backend

# 8. Install nginx config
echo "Installing nginx site..."
sudo cp /tmp/bodega-nginx.conf /etc/nginx/sites-available/bodega
sudo ln -sf /etc/nginx/sites-available/bodega /etc/nginx/sites-enabled/bodega
sudo nginx -t

# 9. Start services
echo "Starting services..."
sudo systemctl start bodega-backend
sudo systemctl reload nginx

echo "✓ Setup complete."
echo "⚠️  Don't forget to:"
echo "  1. Edit /opt/bodega-backend/.env with real Stripe/Resend keys"
echo "  2. Run: sudo systemctl status bodega-backend"
echo "  3. Configure Cloudflare DNS: bodega.aiforlancaster.com → arc-vps IP"

#!/bin/bash

# Teletriage Deployment Script
# Run this on your server to setup automatic deployment

echo "🚀 Setting up Teletriage Deployment..."

# Create deployment directory
sudo mkdir -p /var/www/teletriage
sudo chown $USER:$USER /var/www/teletriage
cd /var/www/teletriage

# Clone repository if not exists
if [ ! -d ".git" ]; then
    git clone https://github.com/michaelgoland1-GLD/Teletriage.git .
else
    git remote set-url origin https://github.com/michaelgoland1-GLD/Teletriage.git
fi

# Pull latest changes
git pull origin main

# Install Python dependencies
pip3 install -r requirements.txt

# Create systemd service
sudo tee /etc/systemd/system/teletriage.service > /dev/null <<EOF
[Unit]
Description=Teletriage Medical Triage System
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/teletriage
Environment=PATH=/usr/bin:/usr/local/bin
ExecStart=/usr/bin/python3 /var/www/teletriage/run_system.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable teletriage
sudo systemctl start teletriage

# Setup firewall (if ufw is active)
if command -v ufw &> /dev/null; then
    sudo ufw allow 8501/tcp  # Streamlit default port
    sudo ufw allow 5000/tcp  # Flask default port
fi

echo "✅ Deployment setup completed!"
echo "📋 Next steps:"
echo "1. Add SSH key to GitHub repository secrets"
echo "2. Configure GitHub repository secrets:"
echo "   - SERVER_HOST: Your server IP/domain"
echo "   - SERVER_USER: SSH username"
echo "   - SERVER_SSH_KEY: Private SSH key"
echo "   - SERVER_PORT: SSH port (default 22)"
echo ""
echo "🌐 Your application will be available at:"
echo "   http://your-server-ip:8501"

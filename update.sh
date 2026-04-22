#!/bin/bash

# Teletriage Simple Auto-Update Script
# Jalankan di server untuk update dari GitHub

echo "🚀 TELETRIAGE AUTO-UPDATE"
echo "=========================="
echo "⏰ $(date)"

# Pindah ke direktori project
cd "$(dirname "$0")"

# Fetch dan pull dari GitHub
echo "📥 Pulling latest changes from GitHub..."
git pull origin main

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Restart service (jika ada)
if systemctl is-active --quiet teletriage; then
    echo "🔄 Restarting teletriage service..."
    sudo systemctl restart teletriage
else
    echo "⚠️ No systemd service found"
    echo "📋 You may need to restart manually:"
    echo "   streamlit run run_system.py"
fi

echo "✅ Update completed at $(date)"

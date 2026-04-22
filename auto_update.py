#!/usr/bin/env python3
"""
Teletriage Auto-Update Script
Jalankan script ini di server untuk auto-update dari GitHub
"""

import subprocess
import os
import sys
from datetime import datetime

def run_command(cmd, description):
    """Execute command and log output"""
    print(f"\n🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print(f"❌ {description} - FAILED")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False

def main():
    print("=" * 50)
    print("🚀 TELETRIAGE AUTO-UPDATE FROM GITHUB")
    print("=" * 50)
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Change to project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    print(f"📁 Working directory: {project_dir}")
    
    # Step 1: Fetch latest changes
    if not run_command("git fetch origin", "Fetching latest changes from GitHub"):
        print("❌ Failed to fetch from GitHub")
        return False
    
    # Step 2: Check if there are updates
    result = subprocess.run("git rev-parse HEAD", shell=True, capture_output=True, text=True)
    current_commit = result.stdout.strip()
    
    result = subprocess.run("git rev-parse origin/main", shell=True, capture_output=True, text=True)
    latest_commit = result.stdout.strip()
    
    if current_commit == latest_commit:
        print("\n✅ Already up to date! No changes to deploy.")
        return True
    
    print(f"\n📢 Update available!")
    print(f"   Current: {current_commit[:7]}")
    print(f"   Latest:  {latest_commit[:7]}")
    
    # Step 3: Pull latest changes
    if not run_command("git pull origin main", "Pulling latest changes"):
        print("❌ Failed to pull from GitHub")
        return False
    
    # Step 4: Install/update dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("❌ Failed to install dependencies")
        return False
    
    # Step 5: Run tests (optional - comment out if not needed)
    print("\n🧪 Running tests...")
    test_result = run_command("cd backend && python test_runner.py", "Running test suite")
    if not test_result:
        print("⚠️ Tests failed, but continuing deployment...")
    
    # Step 6: Restart services (adjust based on your setup)
    print("\n🔄 Restarting services...")
    
    # Check if running with streamlit
    if os.path.exists("run_system.py"):
        print("📋 Streamlit detected - you may need to restart manually")
        print("   Or use: pkill -f streamlit && streamlit run run_system.py")
    
    # Check if running with systemd service
    service_result = run_command("sudo systemctl restart teletriage", "Restarting teletriage service")
    if not service_result:
        print("⚠️ Service restart failed or not configured")
    
    print("\n" + "=" * 50)
    print("✅ AUTO-UPDATE COMPLETED SUCCESSFULLY!")
    print("=" * 50)
    print(f"⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n🌐 Your application should now be running the latest version.")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

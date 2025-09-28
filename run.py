#!/usr/bin/env python3
"""
Mental Health Fitness Tracker - Startup Script
Run this script to start the application
"""

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    return True

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False

def create_upload_directory():
    """Create uploads directory if it doesn't exist"""
    uploads_dir = "uploads"
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
        print(f"📁 Created {uploads_dir} directory")

def main():
    """Main startup function"""
    print("🧠 Mental Health Fitness Tracker")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create uploads directory
    create_upload_directory()
    
    # Install requirements
    if not install_requirements():
        print("⚠️  Warning: Some packages may not be installed correctly")
    
    print("\n🚀 Starting the application...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the server")
    print("=" * 40)
    
    # Start the Flask application
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Quick Deployment Script for Mental Health Fitness Tracker
This script helps you deploy your app in minutes!
"""

import os
import subprocess
import sys
import webbrowser

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {description}: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False

def check_git_status():
    """Check if git is initialized and files are committed"""
    try:
        # Check if git is initialized
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if "not a git repository" in result.stderr:
            print("📁 Initializing Git repository...")
            if not run_command('git init', 'Git initialization'):
                return False
        
        # Check if files are committed
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
        if result.stdout.strip():
            print("📝 Adding and committing files...")
            if not run_command('git add .', 'Adding files to git'):
                return False
            if not run_command('git commit -m "Deploy Mental Health Fitness Tracker"', 'Committing files'):
                return False
        else:
            print("✅ All files are already committed")
        
        return True
    except Exception as e:
        print(f"❌ Error checking git status: {e}")
        return False

def main():
    """Main deployment function"""
    print("🧠 Mental Health Fitness Tracker - Quick Deploy")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print("❌ Error: app.py not found. Please run this script from your project directory.")
        return
    
    print("📋 Pre-deployment checklist:")
    print("✅ app.py - Main Flask application")
    print("✅ requirements.txt - Dependencies")
    print("✅ templates/ - HTML templates")
    print("✅ static/ - CSS and JavaScript files")
    
    # Check git status
    if not check_git_status():
        print("❌ Git setup failed. Please fix the issues above.")
        return
    
    print("\n🚀 Ready for deployment!")
    print("\nChoose your deployment platform:")
    print("1. 🥇 Railway (Recommended - Easiest)")
    print("2. 🥈 Render (Reliable)")
    print("3. 🥉 Heroku (Classic)")
    print("4. 📖 Show manual steps for all platforms")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        deploy_railway()
    elif choice == "2":
        deploy_render()
    elif choice == "3":
        deploy_heroku()
    elif choice == "4":
        show_manual_steps()
    else:
        print("❌ Invalid choice. Please run the script again.")

def deploy_railway():
    """Deploy to Railway"""
    print("\n🥇 DEPLOYING TO RAILWAY")
    print("=" * 40)
    
    print("\n📋 Steps to complete:")
    print("1. Go to: https://railway.app")
    print("2. Click 'Login' → 'Login with GitHub'")
    print("3. Click 'Deploy from GitHub repo'")
    print("4. Select your repository")
    print("5. Click 'Deploy'")
    print("6. Wait 2-3 minutes")
    
    print("\n🌐 Your app will be live at: https://your-app-name.railway.app")
    
    # Open Railway in browser
    webbrowser.open('https://railway.app')
    
    print("\n✅ Railway deployment guide opened in your browser!")

def deploy_render():
    """Deploy to Render"""
    print("\n🥈 DEPLOYING TO RENDER")
    print("=" * 40)
    
    print("\n📋 Steps to complete:")
    print("1. Go to: https://render.com")
    print("2. Sign up with GitHub")
    print("3. Click 'New' → 'Web Service'")
    print("4. Connect your GitHub repository")
    print("5. Configure:")
    print("   - Build Command: pip install -r requirements.txt")
    print("   - Start Command: python app.py")
    print("6. Click 'Create Web Service'")
    print("7. Wait 5-10 minutes")
    
    print("\n🌐 Your app will be live at: https://your-app-name.onrender.com")
    
    # Open Render in browser
    webbrowser.open('https://render.com')
    
    print("\n✅ Render deployment guide opened in your browser!")

def deploy_heroku():
    """Deploy to Heroku"""
    print("\n🥉 DEPLOYING TO HEROKU")
    print("=" * 40)
    
    print("\n📋 Steps to complete:")
    print("1. Install Heroku CLI from: https://devcenter.heroku.com/articles/heroku-cli")
    print("2. Run: heroku login")
    print("3. Run: heroku create your-app-name")
    print("4. Run: git push heroku main")
    print("5. Run: heroku ps:scale web=1")
    
    print("\n🌐 Your app will be live at: https://your-app-name.herokuapp.com")
    
    # Open Heroku in browser
    webbrowser.open('https://heroku.com')
    
    print("\n✅ Heroku deployment guide opened in your browser!")

def show_manual_steps():
    """Show manual deployment steps"""
    print("\n📖 MANUAL DEPLOYMENT STEPS")
    print("=" * 50)
    
    print("\n🥇 RAILWAY (RECOMMENDED):")
    print("1. Go to railway.app")
    print("2. Login with GitHub")
    print("3. Deploy from GitHub repo")
    print("4. Select your repository")
    print("5. Deploy automatically!")
    
    print("\n🥈 RENDER:")
    print("1. Go to render.com")
    print("2. Sign up with GitHub")
    print("3. Create Web Service")
    print("4. Connect repository")
    print("5. Set build/start commands")
    
    print("\n🥉 HEROKU:")
    print("1. Install Heroku CLI")
    print("2. heroku login")
    print("3. heroku create app-name")
    print("4. git push heroku main")
    print("5. heroku ps:scale web=1")
    
    print("\n📚 For detailed instructions, see DEPLOYMENT_GUIDE.md")

if __name__ == "__main__":
    main()

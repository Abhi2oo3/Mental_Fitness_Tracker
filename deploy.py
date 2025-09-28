#!/usr/bin/env python3
"""
Mental Health Fitness Tracker - Deployment Helper
This script helps you prepare and deploy your application
"""

import os
import subprocess
import sys

def check_git():
    """Check if git is available and initialized"""
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Git is available")
            return True
        else:
            print("❌ Git is not available. Please install Git first.")
            return False
    except FileNotFoundError:
        print("❌ Git is not installed. Please install Git first.")
        return False

def check_files():
    """Check if all required files exist"""
    required_files = [
        'app.py',
        'requirements.txt',
        'templates/index.html',
        'static/css/style.css',
        'static/js/app.js'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print("✅ All required files present")
        return True

def create_procfile():
    """Create Procfile for Heroku deployment"""
    procfile_content = "web: python app.py"
    with open('Procfile', 'w') as f:
        f.write(procfile_content)
    print("✅ Created Procfile for Heroku")

def create_runtime():
    """Create runtime.txt for Python version"""
    runtime_content = "python-3.9.7"
    with open('runtime.txt', 'w') as f:
        f.write(runtime_content)
    print("✅ Created runtime.txt")

def create_gitignore():
    """Create .gitignore file"""
    if os.path.exists('.gitignore'):
        print("✅ .gitignore already exists")
        return
    
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Flask
instance/
.webassets-cache

# Uploads
uploads/
*.csv

# Logs
*.log
"""
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    print("✅ Created .gitignore")

def init_git():
    """Initialize git repository if not already initialized"""
    if os.path.exists('.git'):
        print("✅ Git repository already initialized")
        return True
    
    try:
        subprocess.run(['git', 'init'], check=True)
        print("✅ Git repository initialized")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to initialize git repository")
        return False

def add_files():
    """Add files to git"""
    try:
        subprocess.run(['git', 'add', '.'], check=True)
        print("✅ Files added to git")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to add files to git")
        return False

def commit_files():
    """Commit files to git"""
    try:
        subprocess.run(['git', 'commit', '-m', 'Initial commit - Mental Health Fitness Tracker'], check=True)
        print("✅ Files committed to git")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to commit files")
        return False

def show_deployment_options():
    """Show deployment options"""
    print("\n" + "="*60)
    print("🚀 DEPLOYMENT OPTIONS")
    print("="*60)
    print("\n1. 🥇 RAILWAY (RECOMMENDED)")
    print("   - Go to: https://railway.app")
    print("   - Sign up with GitHub")
    print("   - Click 'Deploy from GitHub repo'")
    print("   - Select your repository")
    print("   - Deploy automatically!")
    print("   - Get URL: https://your-app-name.railway.app")
    
    print("\n2. 🥈 RENDER")
    print("   - Go to: https://render.com")
    print("   - Sign up and connect GitHub")
    print("   - Create 'Web Service'")
    print("   - Select your repo")
    print("   - Build Command: pip install -r requirements.txt")
    print("   - Start Command: python app.py")
    print("   - Deploy!")
    
    print("\n3. 🥉 HEROKU")
    print("   - Install Heroku CLI")
    print("   - Run: heroku create your-app-name")
    print("   - Run: git push heroku main")
    print("   - Run: heroku ps:scale web=1")
    
    print("\n4. 🌐 VERCEL")
    print("   - Install: npm i -g vercel")
    print("   - Run: vercel")
    print("   - Follow prompts")
    
    print("\n5. 🐍 PYTHONANYWHERE")
    print("   - Go to: https://pythonanywhere.com")
    print("   - Upload files")
    print("   - Configure web app")

def main():
    """Main deployment helper function"""
    print("🧠 Mental Health Fitness Tracker - Deployment Helper")
    print("="*60)
    
    # Check prerequisites
    if not check_git():
        print("\n❌ Please install Git first: https://git-scm.com/downloads")
        return
    
    if not check_files():
        print("\n❌ Please ensure all required files are present")
        return
    
    # Create deployment files
    print("\n📁 Creating deployment files...")
    create_procfile()
    create_runtime()
    create_gitignore()
    
    # Initialize git if needed
    print("\n🔧 Setting up Git...")
    if not init_git():
        return
    
    # Add and commit files
    if not add_files():
        return
    
    if not commit_files():
        return
    
    print("\n✅ Repository ready for deployment!")
    print("\n📤 Next steps:")
    print("1. Create a GitHub repository")
    print("2. Push your code: git remote add origin <your-repo-url>")
    print("3. Push: git push -u origin main")
    print("4. Choose a deployment platform from the options below")
    
    # Show deployment options
    show_deployment_options()
    
    print("\n🎉 Your Mental Health Fitness Tracker is ready to deploy!")
    print("🌍 Once deployed, it will be accessible worldwide!")

if __name__ == "__main__":
    main()

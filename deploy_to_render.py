#!/usr/bin/env python3
"""
Deployment helper script for AgriSmart NDVI Model
This script helps prepare and verify the deployment configuration
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def check_required_files():
    """Check if all required files exist for deployment"""
    required_files = [
        'render.yaml',
        'Procfile', 
        'requirements-prod.txt',
        'src/app_prod.py',
        'src/gee_integration.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    
    print("✅ All required files present")
    return True

def check_git_status():
    """Check git status and suggest commits"""
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        
        if result.stdout.strip():
            print("⚠️  Uncommitted changes detected:")
            print(result.stdout)
            print("\n💡 Consider running:")
            print("   git add .")
            print("   git commit -m 'Prepare for Render deployment'")
            print("   git push origin main")
            return False
        else:
            print("✅ Git working directory clean")
            return True
    except Exception as e:
        print(f"⚠️  Could not check git status: {e}")
        return True

def verify_render_config():
    """Verify render.yaml configuration"""
    try:
        with open('render.yaml', 'r') as f:
            content = f.read()
            
        if 'GEE_MODE' in content and 'live' in content:
            print("✅ Render configuration includes GEE live mode")
        else:
            print("⚠️  GEE live mode not found in render.yaml")
            
        if 'gunicorn' in content:
            print("✅ Gunicorn configuration found")
        else:
            print("⚠️  Gunicorn configuration missing")
            
        return True
    except Exception as e:
        print(f"❌ Error reading render.yaml: {e}")
        return False

def test_local_app():
    """Test if the application runs locally"""
    try:
        print("🧪 Testing local application...")
        result = subprocess.run([
            sys.executable, '-c', 
            'import sys; sys.path.append("src"); from app_prod import app; print("✅ App imports successfully")'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Local application test passed")
            return True
        else:
            print(f"❌ Local application test failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error testing local app: {e}")
        return False

def generate_deployment_summary():
    """Generate deployment summary"""
    print("\n" + "="*60)
    print("🚀 AGRISMART DEPLOYMENT SUMMARY")
    print("="*60)
    
    print("\n📋 Next Steps:")
    print("1. Go to https://dashboard.render.com/")
    print("2. Click 'New +' > 'Web Service'")
    print("3. Connect your Git repository")
    print("4. Use these settings:")
    print("   - Build Command: pip install -r requirements-prod.txt")
    print("   - Start Command: gunicorn src.app_prod:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120")
    print("5. Set environment variables:")
    print("   - GEE_MODE=live")
    print("   - GEE_PROJECT=crested-primacy-471013-r0")
    print("   - FLASK_ENV=production")
    print("   - PYTHONPATH=.")
    
    print("\n🔐 GEE Authentication:")
    print("Option 1 (Recommended): Use service account")
    print("  - Create service account in Google Cloud Console")
    print("  - Download JSON key file")
    print("  - Add GOOGLE_APPLICATION_CREDENTIALS environment variable")
    
    print("\nOption 2: Use personal authentication")
    print("  - Deploy first, then use Render shell")
    print("  - Run: earthengine authenticate")
    
    print("\n📊 Test Endpoints:")
    print("  - Health: https://your-app.onrender.com/health")
    print("  - Predict: https://your-app.onrender.com/predict-gee")
    print("  - Dashboard: https://your-app.onrender.com/dashboard")
    
    print("\n📚 Full Guide: See DEPLOYMENT_GUIDE.md")
    print("="*60)

def main():
    """Main deployment preparation function"""
    print("🔍 Preparing AgriSmart for Render deployment...\n")
    
    checks = [
        ("Required Files", check_required_files),
        ("Git Status", check_git_status),
        ("Render Config", verify_render_config),
        ("Local App Test", test_local_app)
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        print(f"\n🔍 {check_name}:")
        if not check_func():
            all_passed = False
    
    if all_passed:
        print("\n✅ All checks passed! Ready for deployment.")
    else:
        print("\n⚠️  Some checks failed. Please fix issues before deploying.")
    
    generate_deployment_summary()

if __name__ == "__main__":
    main()

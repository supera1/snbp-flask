#!/usr/bin/env python3
"""
Helper script to set up environment variable from service-account.json file
This makes it easy to test locally and prepare for cloud deployment
"""

import json
import os
import sys

def main():
    # Check if service-account.json exists
    if not os.path.exists('service-account.json'):
        print("❌ Error: service-account.json not found!")
        print("Please place your Google service account JSON file in the current directory.")
        sys.exit(1)
    
    # Read the service account file
    try:
        with open('service-account.json', 'r') as f:
            service_account_data = json.load(f)
        
        # Convert to compact JSON string
        json_string = json.dumps(service_account_data, separators=(',', ':'))
        
        print("✅ Service account JSON loaded successfully!")
        print("\n" + "="*60)
        print("ENVIRONMENT VARIABLE SETUP")
        print("="*60)
        
        # Instructions for different platforms
        print("\n🔧 For local testing (bash/zsh):")
        print(f"export GOOGLE_SERVICE_ACCOUNT='{json_string}'")
        
        print("\n🔧 For local testing (Windows PowerShell):")
        print(f'$env:GOOGLE_SERVICE_ACCOUNT=\'{json_string}\'')
        
        print("\n🔧 For local testing (Windows CMD):")
        print(f'set GOOGLE_SERVICE_ACCOUNT={json_string}')
        
        print("\n📋 For cloud platforms (copy this value):")
        print("-" * 60)
        print(json_string)
        print("-" * 60)
        
        print("\n📝 Platform-specific instructions:")
        print("• Render.com: Dashboard → Environment → Add 'GOOGLE_SERVICE_ACCOUNT'")
        print("• PythonAnywhere: In WSGI config file")
        print("• Vercel: Settings → Environment Variables")
        print("• Railway: Variables → Add 'GOOGLE_SERVICE_ACCOUNT'")
        
        # Create .env file for local development
        print("\n💡 Creating .env file for local development...")
        with open('.env', 'w') as f:
            f.write(f"GOOGLE_SERVICE_ACCOUNT='{json_string}'\n")
        print("✅ .env file created successfully!")
        
        print("\n⚠️  IMPORTANT: Never commit service-account.json or .env to Git!")
        print("Make sure both are in your .gitignore file.")
        
    except json.JSONDecodeError:
        print("❌ Error: Invalid JSON in service-account.json")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
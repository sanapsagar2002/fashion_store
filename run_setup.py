#!/usr/bin/env python
"""
Quick setup script for Fashion Store
This script will run all necessary Django commands to set up the project
"""

import os
import sys
import subprocess

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {description}: {e.stderr}")
        return False

def main():
    """Main setup function"""
    print("🚀 Fashion Store - Quick Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Install requirements
    if not run_command("pip install -r requirements.txt", "Installing requirements"):
        print("❌ Failed to install requirements. Please check your Python environment.")
        sys.exit(1)
    
    # Make migrations
    if not run_command("python manage.py makemigrations", "Creating migrations"):
        print("❌ Failed to create migrations")
        sys.exit(1)
    
    # Run migrations
    if not run_command("python manage.py migrate", "Running migrations"):
        print("❌ Failed to run migrations")
        sys.exit(1)
    
    # Create superuser (non-interactive)
    print("🔄 Creating superuser...")
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@fashionstore.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            print("✅ Superuser created: admin@fashionstore.com / admin123")
        else:
            print("ℹ️  Superuser already exists")
    except Exception as e:
        print(f"⚠️  Could not create superuser: {e}")
    
    # Run database setup
    print("🔄 Setting up sample data...")
    if not run_command("python setup_database.py", "Setting up sample data"):
        print("⚠️  Sample data setup failed, but you can continue")
    
    print("=" * 50)
    print("✅ Setup completed successfully!")
    print("\n📋 Your Fashion Store is ready!")
    print("\n🌐 Access your application:")
    print("   • Website: http://localhost:8000")
    print("   • Admin: http://localhost:8000/admin/")
    print("   • API: http://localhost:8000/api/")
    print("\n👤 Admin credentials:")
    print("   • Email: admin@fashionstore.com")
    print("   • Password: admin123")
    print("\n🚀 To start the server, run:")
    print("   python manage.py runserver")
    print("\n📚 For more information, see README.md")

if __name__ == '__main__':
    main()


#!/usr/bin/env python
"""
Test MySQL Database Connection
Run this script to test if your database credentials are correct
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fashion_store.settings')
django.setup()

from django.db import connection
from django.core.exceptions import ImproperlyConfigured

def test_database_connection():
    """Test the database connection"""
    print("🔧 Testing Database Connection")
    print("=" * 40)
    
    try:
        # Test the connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            
        print("✅ Database connection successful!")
        print("✅ Database 'fashion_store_db' is accessible")
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure MySQL is running")
        print("2. Check your database credentials in fashion_store/settings.py")
        print("3. Ensure the database 'fashion_store_db' exists")
        print("4. Verify your MySQL username and password")
        return False

if __name__ == "__main__":
    if test_database_connection():
        print("\n🎉 Database is ready! You can now run migrations.")
        print("Next steps:")
        print("1. python manage.py makemigrations")
        print("2. python manage.py migrate")
        print("3. python setup_database.py")
    else:
        print("\n❌ Please fix the database connection issues first.")
        sys.exit(1)


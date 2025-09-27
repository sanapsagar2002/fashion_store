#!/usr/bin/env python
"""
MySQL Database Setup Script for Fashion Store
This script will help you create the database and test the connection
"""

import pymysql
import sys

def test_mysql_connection():
    """Test MySQL connection with user-provided credentials"""
    print("🔧 MySQL Database Setup for Fashion Store")
    print("=" * 50)
    
    # Get database credentials from user
    print("Please enter your MySQL credentials:")
    host = input("MySQL Host (default: localhost): ").strip() or "localhost"
    port = input("MySQL Port (default: 3306): ").strip() or "3306"
    user = input("MySQL Username (default: root): ").strip() or "root"
    password = input("MySQL Password: ").strip()
    
    if not password:
        print("❌ Password is required!")
        return False
    
    try:
        # Test connection
        print("\n🔄 Testing MySQL connection...")
        connection = pymysql.connect(
            host=host,
            port=int(port),
            user=user,
            password=password
        )
        
        print("✅ MySQL connection successful!")
        
        # Create database
        print("🔄 Creating database 'fashion_store_db'...")
        with connection.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS fashion_store_db")
            print("✅ Database 'fashion_store_db' created successfully!")
        
        connection.close()
        
        # Update settings.py with the credentials
        print("\n🔄 Updating Django settings...")
        update_django_settings(host, port, user, password)
        
        print("\n✅ Database setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Run: python manage.py makemigrations")
        print("2. Run: python manage.py migrate")
        print("3. Run: python setup_database.py")
        print("4. Run: python manage.py runserver")
        
        return True
        
    except pymysql.Error as e:
        print(f"❌ MySQL Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def update_django_settings(host, port, user, password):
    """Update Django settings with the provided credentials"""
    settings_file = "fashion_store/settings.py"
    
    try:
        with open(settings_file, 'r') as f:
            content = f.read()
        
        # Replace the database configuration
        old_config = """DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fashion_store_db',
        'USER': 'root',  # Change this to your MySQL username
        'PASSWORD': 'your_mysql_password',  # Change this to your MySQL password
        'HOST': 'localhost',
        'PORT': '3306',
    }
}"""
        
        new_config = f"""DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fashion_store_db',
        'USER': '{user}',
        'PASSWORD': '{password}',
        'HOST': '{host}',
        'PORT': '{port}',
    }}
}}"""
        
        content = content.replace(old_config, new_config)
        
        with open(settings_file, 'w') as f:
            f.write(content)
        
        print("✅ Django settings updated with your MySQL credentials")
        
    except Exception as e:
        print(f"⚠️  Could not update settings automatically: {e}")
        print("Please manually update the database credentials in fashion_store/settings.py")

if __name__ == "__main__":
    if test_mysql_connection():
        print("\n🎉 Setup completed! You can now run the Django commands.")
    else:
        print("\n❌ Setup failed. Please check your MySQL credentials and try again.")
        sys.exit(1)


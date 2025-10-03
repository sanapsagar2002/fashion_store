#!/usr/bin/env python
"""
Database setup script for Fashion Store
Run this script to create initial data for the application
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fashion_store.settings')
django.setup()

from django.contrib.auth import get_user_model
from products.models import Category, Product, ProductImage, ProductVariant
from orders.models import DiscountCode
from datetime import datetime, timedelta

User = get_user_model()

def create_superuser():
    """Create a superuser if it doesn't exist"""
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@fashionstore.com',
            password='admin123',
            first_name='Admin',
            last_name='User'
        )
        print("Superuser created: admin@fashionstore.com / admin123")
    else:
        print("Superuser already exists")

def create_categories():
    """Create product categories"""
    categories_data = [
        {'name': 'T-Shirts', 'description': 'Comfortable and stylish t-shirts'},
        {'name': 'Jeans', 'description': 'Classic and modern jeans'},
        {'name': 'Dresses', 'description': 'Elegant and trendy dresses'},
        {'name': 'Shoes', 'description': 'Comfortable and fashionable shoes'},
        {'name': 'Accessories', 'description': 'Stylish accessories and jewelry'},
        {'name': 'Jackets', 'description': 'Warm and stylish jackets'},
    ]
    
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        if created:
            print(f"Created category: {category.name}")
        else:
            print(f"Category already exists: {category.name}")

def create_sample_products():
    """Create sample products with variants"""
    # Get categories
    tshirts = Category.objects.get(name='T-Shirts')
    jeans = Category.objects.get(name='Jeans')
    dresses = Category.objects.get(name='Dresses')
    shoes = Category.objects.get(name='Shoes')
    
    products_data = [
        {
            'name': 'Classic White T-Shirt',
            'description': 'A comfortable and versatile white t-shirt perfect for any occasion.',
            'price': 19.99,
            'category': tshirts,
            'gender': 'U',
            'brand': 'Fashion Store',
            'variants': [
                {'size': 'S', 'color': 'White', 'stock_quantity': 50},
                {'size': 'M', 'color': 'White', 'stock_quantity': 75},
                {'size': 'L', 'color': 'White', 'stock_quantity': 60},
                {'size': 'XL', 'color': 'White', 'stock_quantity': 40},
            ]
        },
        {
            'name': 'Blue Denim Jeans',
            'description': 'Classic blue denim jeans with a modern fit.',
            'price': 59.99,
            'category': jeans,
            'gender': 'M',
            'brand': 'Fashion Store',
            'variants': [
                {'size': 'S', 'color': 'Blue', 'stock_quantity': 30},
                {'size': 'M', 'color': 'Blue', 'stock_quantity': 45},
                {'size': 'L', 'color': 'Blue', 'stock_quantity': 50},
                {'size': 'XL', 'color': 'Blue', 'stock_quantity': 35},
            ]
        },
        {
            'name': 'Summer Floral Dress',
            'description': 'Beautiful floral dress perfect for summer days.',
            'price': 79.99,
            'category': dresses,
            'gender': 'W',
            'brand': 'Fashion Store',
            'variants': [
                {'size': 'S', 'color': 'Floral', 'stock_quantity': 25},
                {'size': 'M', 'color': 'Floral', 'stock_quantity': 40},
                {'size': 'L', 'color': 'Floral', 'stock_quantity': 35},
                {'size': 'XL', 'color': 'Floral', 'stock_quantity': 20},
            ]
        },
        {
            'name': 'Comfortable Sneakers',
            'description': 'Comfortable and stylish sneakers for everyday wear.',
            'price': 89.99,
            'category': shoes,
            'gender': 'U',
            'brand': 'Fashion Store',
            'variants': [
                {'size': 'S', 'color': 'White', 'stock_quantity': 40},
                {'size': 'M', 'color': 'White', 'stock_quantity': 60},
                {'size': 'L', 'color': 'White', 'stock_quantity': 55},
                {'size': 'XL', 'color': 'White', 'stock_quantity': 30},
            ]
        },
        {
            'name': 'Black Leather Jacket',
            'description': 'Stylish black leather jacket for a cool look.',
            'price': 149.99,
            'category': Category.objects.get(name='Jackets'),
            'gender': 'U',
            'brand': 'Fashion Store',
            'variants': [
                {'size': 'S', 'color': 'Black', 'stock_quantity': 20},
                {'size': 'M', 'color': 'Black', 'stock_quantity': 30},
                {'size': 'L', 'color': 'Black', 'stock_quantity': 25},
                {'size': 'XL', 'color': 'Black', 'stock_quantity': 15},
            ]
        }
    ]
    
    for product_data in products_data:
        variants = product_data.pop('variants')
        product, created = Product.objects.get_or_create(
            name=product_data['name'],
            defaults=product_data
        )
        
        if created:
            print(f"Created product: {product.name}")
            
            # Create variants
            for variant_data in variants:
                size = variant_data['size']
                color = variant_data['color']
                sku = f"{product.name.replace(' ', '').upper()}-{size}-{color.upper()}"
                ProductVariant.objects.create(
                    product=product,
                    sku=sku,
                    **variant_data
                )
            
            # Create a primary image (placeholder)
            ProductImage.objects.create(
                product=product,
                image='products/placeholder.jpg',  # This would be a real image in production
                is_primary=True
            )
        else:
            print(f"Product already exists: {product.name}")

def create_discount_codes():
    """Create sample discount codes"""
    discount_codes = [
        {
            'code': 'WELCOME10',
            'description': 'Welcome discount for new customers',
            'discount_type': 'percentage',
            'discount_value': 10.00,
            'minimum_order_amount': 50.00,
            'max_uses': 100,
            'valid_from': datetime.now(),
            'valid_until': datetime.now() + timedelta(days=30)
        },
        {
            'code': 'SAVE20',
            'description': 'Save $20 on orders over $100',
            'discount_type': 'fixed',
            'discount_value': 20.00,
            'minimum_order_amount': 100.00,
            'max_uses': 50,
            'valid_from': datetime.now(),
            'valid_until': datetime.now() + timedelta(days=60)
        }
    ]
    
    for code_data in discount_codes:
        discount, created = DiscountCode.objects.get_or_create(
            code=code_data['code'],
            defaults=code_data
        )
        if created:
            print(f"Created discount code: {discount.code}")
        else:
            print(f"Discount code already exists: {discount.code}")

def main():
    """Main setup function"""
    print("Setting up Fashion Store database...")
    print("=" * 50)
    
    try:
        create_superuser()
        create_categories()
        create_sample_products()
        create_discount_codes()
        
        print("=" * 50)
        print("Database setup completed successfully!")
        print("\nNext steps:")
        print("1. Run: python manage.py runserver")
        print("2. Visit: http://localhost:8000")
        print("3. Admin panel: http://localhost:8000/admin/")
        print("4. Login with: admin@fashionstore.com / admin123")
        
    except Exception as e:
        print(f"Error during setup: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

#!/usr/bin/env python
"""
Script to download and set up proper product images for each product
"""
import os
import shutil
import requests
from pathlib import Path
from django.core.management import execute_from_command_line
import django
import sys

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fashion_store.settings')
django.setup()

from products.models import Product, ProductImage

def download_image(url, filepath):
    """Download an image from URL to filepath"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def create_product_images():
    """Create proper images for each product"""
    media_path = Path('media/products')
    media_path.mkdir(parents=True, exist_ok=True)
    
    # Image URLs for different product types
    image_urls = {
        't-shirt': [
            'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
            'https://images.unsplash.com/photo-1503341504253-dff4815485f1?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
            'https://images.unsplash.com/photo-1583743814966-8936f37f0c6e?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80'
        ],
        'jeans': [
            'https://images.unsplash.com/photo-1542272604-787c3835535d?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
            'https://images.unsplash.com/photo-1475178626620-a4d074967452?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
            'https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80'
        ],
        'dress': [
            'https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
            'https://images.unsplash.com/photo-1566479179817-c0d9de9d65d1?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
            'https://images.unsplash.com/photo-1594736797933-d0401ba2fe65?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80'
        ],
        'sneakers': [
            'https://images.unsplash.com/photo-1549298916-b41d501d3772?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
            'https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
            'https://images.unsplash.com/photo-1608231387042-66d1773070a5?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80'
        ],
        'jacket': [
            'https://images.unsplash.com/photo-1551028719-00167b16eac5?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
            'https://images.unsplash.com/photo-1591047139829-d91aecb6caea?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
            'https://images.unsplash.com/photo-1551488831-00ddcb6c6bd3?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80'
        ]
    }
    
    print("Downloading product images...")
    
    # Get all products
    products = Product.objects.all()
    
    for i, product in enumerate(products, 1):
        print(f"Processing product {i}: {product.name}")
        
        # Determine product type for image selection
        product_type = 't-shirt'  # default
        if 'jean' in product.name.lower():
            product_type = 'jeans'
        elif 'dress' in product.name.lower():
            product_type = 'dress'
        elif 'sneaker' in product.name.lower():
            product_type = 'sneakers'
        elif 'jacket' in product.name.lower():
            product_type = 'jacket'
        
        # Skip leather bag/jacket as requested
        if 'leather' in product.name.lower() and 'bag' in product.name.lower():
            print(f"Skipping leather bag: {product.name}")
            continue
        
        # Get images for this product type
        urls = image_urls.get(product_type, image_urls['t-shirt'])
        
        # Download primary image
        primary_filename = f"product_{product.id}_primary.jpg"
        primary_path = media_path / primary_filename
        
        if download_image(urls[0], primary_path):
            print(f"Downloaded primary image: {primary_filename}")
            
            # Update or create ProductImage
            product_image, created = ProductImage.objects.get_or_create(
                product=product,
                is_primary=True,
                defaults={
                    'image': f'products/{primary_filename}',
                    'alt_text': f'{product.name} - Primary Image'
                }
            )
            
            if not created:
                product_image.image = f'products/{primary_filename}'
                product_image.alt_text = f'{product.name} - Primary Image'
                product_image.save()
        
        # Download additional images
        for j, url in enumerate(urls[1:], 1):
            additional_filename = f"product_{product.id}_additional_{j}.jpg"
            additional_path = media_path / additional_filename
            
            if download_image(url, additional_path):
                print(f"Downloaded additional image: {additional_filename}")
                
                # Create additional ProductImage
                ProductImage.objects.get_or_create(
                    product=product,
                    image=f'products/{additional_filename}',
                    defaults={
                        'alt_text': f'{product.name} - Additional Image {j}',
                        'is_primary': False,
                        'order': j
                    }
                )
    
    # Create default image if it doesn't exist
    default_path = media_path / 'default.jpg'
    if not default_path.exists():
        # Copy the first t-shirt image as default
        first_product = Product.objects.first()
        if first_product and first_product.images.exists():
            primary_image = first_product.images.filter(is_primary=True).first()
            if primary_image:
                shutil.copy2(media_path / primary_image.image.name.split('/')[-1], default_path)
                print("Created default.jpg")
    
    print("Product images setup completed!")

if __name__ == "__main__":
    create_product_images()

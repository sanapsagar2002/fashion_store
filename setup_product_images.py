#!/usr/bin/env python
"""
Script to set up proper product images using existing images
"""
import os
import shutil
from pathlib import Path
import django
import sys

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fashion_store.settings')
django.setup()

from products.models import Product, ProductImage

def setup_product_images():
    """Set up proper images for each product using existing images"""
    media_path = Path('media/products')
    media_path.mkdir(parents=True, exist_ok=True)
    
    print("Setting up product images...")
    
    # Get all products
    products = Product.objects.all()
    
    # Image mapping based on product names and categories
    image_mappings = {
        't-shirt': ['classic_white_t-shirt_1.jpg', 'classic_white_t-shirt_2.jpg'],
        'jeans': ['blue_denim_jeans_1.jpg', 'blue_denim_jeans_2.jpg'],
        'dress': ['elegant_black_dress_1.jpg', 'summer_floral_dress_1.jpg'],
        'sneakers': ['comfortable_sneakers_1.jpg', 'comfortable_sneakers_2.jpg'],
        'shoes': ['comfortable_sneakers_1.jpg', 'comfortable_sneakers_2.jpg'],
        'watch': ['elegant_womens_watch_1.jpg', 'digital_sports_watch_1.jpg'],
        'jacket': ['black_leather_jacket_1.jpg', 'black_leather_jacket_2.jpg'],
        'shorts': ['kids_denim_shorts_1.jpg', 'kids_denim_shorts_2.jpg'],
        'blouse': ['floral_summer_blouse_1.jpg', 'floral_summer_blouse_2.jpg'],
        'handbag': ['leather_handbag_1.jpg', 'leather_handbag_2.jpg']
    }
    
    for i, product in enumerate(products, 1):
        print(f"Processing product {i}: {product.name}")
        
        # Determine product type for image selection
        product_name_lower = product.name.lower()
        product_type = 't-shirt'  # default
        
        if 'jean' in product_name_lower:
            product_type = 'jeans'
        elif 'dress' in product_name_lower:
            product_type = 'dress'
        elif 'sneaker' in product_name_lower or 'running' in product_name_lower:
            product_type = 'sneakers'
        elif 'watch' in product_name_lower:
            product_type = 'watch'
        elif 'jacket' in product_name_lower:
            product_type = 'jacket'
        elif 'short' in product_name_lower:
            product_type = 'shorts'
        elif 'blouse' in product_name_lower:
            product_type = 'blouse'
        elif 'handbag' in product_name_lower or 'bag' in product_name_lower:
            product_type = 'handbag'
        elif 'shirt' in product_name_lower or 't-shirt' in product_name_lower:
            product_type = 't-shirt'
        
        # Skip leather bag as requested
        if 'leather' in product_name_lower and 'bag' in product_name_lower:
            print(f"Skipping leather bag: {product.name}")
            continue
        
        # Get images for this product type
        available_images = image_mappings.get(product_type, image_mappings['t-shirt'])
        
        # Use existing images or create new ones
        for j, image_name in enumerate(available_images):
            source_path = media_path / image_name
            
            # If source doesn't exist, use a default image
            if not source_path.exists():
                # Find any existing image to use as base
                existing_images = list(media_path.glob('*.jpg'))
                if existing_images:
                    source_path = existing_images[0]
                else:
                    print(f"No source image found for {image_name}")
                    continue
            
            # Create product-specific image
            if j == 0:
                # Primary image
                dest_filename = f"product_{product.id}_primary.jpg"
                dest_path = media_path / dest_filename
                
                if not dest_path.exists():
                    shutil.copy2(source_path, dest_path)
                    print(f"Created primary image: {dest_filename}")
                
                # Update or create ProductImage
                product_image, created = ProductImage.objects.get_or_create(
                    product=product,
                    is_primary=True,
                    defaults={
                        'image': f'products/{dest_filename}',
                        'alt_text': f'{product.name} - Primary Image'
                    }
                )
                
                if not created:
                    product_image.image = f'products/{dest_filename}'
                    product_image.alt_text = f'{product.name} - Primary Image'
                    product_image.save()
            else:
                # Additional images
                dest_filename = f"product_{product.id}_additional_{j}.jpg"
                dest_path = media_path / dest_filename
                
                if not dest_path.exists():
                    shutil.copy2(source_path, dest_path)
                    print(f"Created additional image: {dest_filename}")
                
                # Create additional ProductImage
                ProductImage.objects.get_or_create(
                    product=product,
                    image=f'products/{dest_filename}',
                    defaults={
                        'alt_text': f'{product.name} - Additional Image {j}',
                        'is_primary': False,
                        'order': j
                    }
                )
    
    # Create default image if it doesn't exist
    default_path = media_path / 'default.jpg'
    if not default_path.exists():
        # Copy the first available image as default
        existing_images = list(media_path.glob('*.jpg'))
        if existing_images:
            shutil.copy2(existing_images[0], default_path)
            print("Created default.jpg")
    
    print("Product images setup completed!")

if __name__ == "__main__":
    setup_product_images()

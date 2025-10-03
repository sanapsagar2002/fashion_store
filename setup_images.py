#!/usr/bin/env python
"""
Script to set up proper product images
"""
import os
import shutil
from pathlib import Path

def create_product_images():
    """Create appropriate product images by copying and renaming existing ones"""
    media_path = Path('media/products')
    
    # Ensure media directory exists
    media_path.mkdir(parents=True, exist_ok=True)
    
    # Image mappings for different product types
    image_mappings = {
        # Sneakers (Kids Running Shoes)
        'sneaker_kids': ['comfortable_sneakers_1.jpg', 'comfortable_sneakers_2.jpg'],
        
        # Shirts for different categories
        't_shirt_men': ['classic_white_t-shirt_1.jpg'],
        't_shirt_women': ['classic_white_t-shirt_1.jpg'],
        't_shirt_kids': ['classic_white_t-shirt_1.jpg'],
        
        # Jeans
        'jeans_men': ['blue_denim_jeans_1.jpg', 'blue_denim_jeans_2.jpg'],
        'jeans_women': ['blue_denim_jeans_1.jpg', 'blue_denim_jeans_2.jpg'],
        
        # Dresses
        'dress_women': ['elegant_black_dress_1.jpg'],
        
        # Default/Watch images
        'watch': ['classic_white_t-shirt_1.jpg'],  # Using t-shirt as placeholder until we get proper watch images
    }
    
    print("Setting up product images...")
    
    # Copy existing images with proper names for better product categorization
    for category, source_files in image_mappings.items():
        for i, source_file in enumerate(source_files):
            source_path = media_path / source_file
            if source_path.exists():
                dest_name = f"{category}_{i+1}.jpg"
                dest_path = media_path / dest_name
                
                if not dest_path.exists():
                    shutil.copy2(source_path, dest_path)
                    print(f"Created: {dest_name}")
                else:
                    print(f"Already exists: {dest_name}")
            else:
                print(f"Source not found: {source_file}")
    
    # Ensure default.jpg exists
    default_source = media_path / 'classic_white_t-shirt_1.jpg'
    default_dest = media_path / 'default.jpg'
    
    if default_source.exists() and not default_dest.exists():
        shutil.copy2(default_source, default_dest)
        print("Created default.jpg")
    
    print("Product images setup completed!")

if __name__ == "__main__":
    create_product_images()
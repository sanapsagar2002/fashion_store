from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from products.models import Category, Product, ProductImage, ProductVariant
import requests
from io import BytesIO


class Command(BaseCommand):
    help = 'Populate database with sample products and images'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create categories
        categories_data = [
            {'name': 'T-Shirts', 'description': 'Comfortable and stylish t-shirts'},
            {'name': 'Jeans', 'description': 'Classic and modern jeans'},
            {'name': 'Dresses', 'description': 'Elegant and trendy dresses'},
            {'name': 'Shoes', 'description': 'Comfortable and fashionable footwear'},
            {'name': 'Accessories', 'description': 'Stylish accessories to complete your look'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Sample products data
        products_data = [
            {
                'name': 'Classic White T-Shirt',
                'description': 'A comfortable and versatile white t-shirt perfect for any occasion.',
                'price': 29.99,
                'category': 'T-Shirts',
                'gender': 'U',
                'brand': 'Fashion Store',
                'images': [
                    'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500',
                    'https://images.unsplash.com/photo-1576566588028-43d2d8a1b0b1?w=500'
                ],
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
                'price': 79.99,
                'category': 'Jeans',
                'gender': 'U',
                'brand': 'Denim Co',
                'images': [
                    'https://images.unsplash.com/photo-1542272604-787c3835535d?w=500',
                    'https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=500'
                ],
                'variants': [
                    {'size': 'S', 'color': 'Blue', 'stock_quantity': 30},
                    {'size': 'M', 'color': 'Blue', 'stock_quantity': 45},
                    {'size': 'L', 'color': 'Blue', 'stock_quantity': 35},
                    {'size': 'XL', 'color': 'Blue', 'stock_quantity': 25},
                ]
            },
            {
                'name': 'Elegant Black Dress',
                'description': 'A sophisticated black dress perfect for formal occasions.',
                'price': 129.99,
                'category': 'Dresses',
                'gender': 'W',
                'brand': 'Elegance',
                'images': [
                    'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=500',
                    'https://images.unsplash.com/photo-1566479179817-c0d9d0b8b5b5?w=500'
                ],
                'variants': [
                    {'size': 'S', 'color': 'Black', 'stock_quantity': 20},
                    {'size': 'M', 'color': 'Black', 'stock_quantity': 30},
                    {'size': 'L', 'color': 'Black', 'stock_quantity': 25},
                    {'size': 'XL', 'color': 'Black', 'stock_quantity': 15},
                ]
            },
            {
                'name': 'Comfortable Sneakers',
                'description': 'Stylish and comfortable sneakers for everyday wear.',
                'price': 89.99,
                'category': 'Shoes',
                'gender': 'U',
                'brand': 'Sneaker Co',
                'images': [
                    'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=500',
                    'https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=500'
                ],
                'variants': [
                    {'size': 'S', 'color': 'White', 'stock_quantity': 40},
                    {'size': 'M', 'color': 'White', 'stock_quantity': 50},
                    {'size': 'L', 'color': 'White', 'stock_quantity': 45},
                    {'size': 'XL', 'color': 'White', 'stock_quantity': 35},
                ]
            },
            {
                'name': 'Leather Handbag',
                'description': 'Premium leather handbag with elegant design.',
                'price': 149.99,
                'category': 'Accessories',
                'gender': 'W',
                'brand': 'Luxury Bags',
                'images': [
                    'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500',
                    'https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=500'
                ],
                'variants': [
                    {'size': 'M', 'color': 'Brown', 'stock_quantity': 15},
                    {'size': 'M', 'color': 'Black', 'stock_quantity': 20},
                ]
            }
        ]
        
        for product_data in products_data:
            # Create product
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults={
                    'description': product_data['description'],
                    'price': product_data['price'],
                    'category': categories[product_data['category']],
                    'gender': product_data['gender'],
                    'brand': product_data['brand'],
                }
            )
            
            if created:
                self.stdout.write(f'Created product: {product.name}')
                
                # Add images
                for i, image_url in enumerate(product_data['images']):
                    try:
                        response = requests.get(image_url, timeout=10)
                        if response.status_code == 200:
                            image_content = ContentFile(response.content)
                            image_content.name = f'{product.name.lower().replace(" ", "_")}_{i+1}.jpg'
                            
                            product_image = ProductImage.objects.create(
                                product=product,
                                image=image_content,
                                is_primary=(i == 0)
                            )
                            self.stdout.write(f'  Added image: {product_image.image.name}')
                    except Exception as e:
                        self.stdout.write(f'  Failed to download image {image_url}: {e}')
                
                # Add variants
                for variant_data in product_data['variants']:
                    ProductVariant.objects.create(
                        product=product,
                        size=variant_data['size'],
                        color=variant_data['color'],
                        stock_quantity=variant_data['stock_quantity']
                    )
                    self.stdout.write(f'  Added variant: {variant_data["size"]} {variant_data["color"]}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample data!')
        )

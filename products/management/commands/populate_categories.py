from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from products.models import Category, Product, ProductVariant, ProductImage
from decimal import Decimal
import os

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate database with Men, Women, Kids categories and accessories (Watch, Sneaker)'

    def handle(self, *args, **options):
        self.stdout.write('Creating categories and sample products...')

        # Create categories
        categories_data = [
            {'name': 'Men\'s Fashion', 'description': 'Trendy men\'s clothing and accessories'},
            {'name': 'Women\'s Fashion', 'description': 'Elegant women\'s clothing and accessories'},
            {'name': 'Kids Fashion', 'description': 'Fun and comfortable kids\' clothing'},
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

        # Create sample products for Men's Fashion
        men_products = [
            {
                'name': 'Classic White T-Shirt',
                'description': 'Premium cotton t-shirt perfect for everyday wear',
                'price': Decimal('29.99'),
                'original_price': Decimal('39.99'),
                'category': categories['Men\'s Fashion'],
                'gender': 'M',
                'brand': 'Nike',
                'is_featured': True,
            },
            {
                'name': 'Blue Denim Jeans',
                'description': 'Comfortable and stylish denim jeans',
                'price': Decimal('79.99'),
                'original_price': Decimal('99.99'),
                'category': categories['Men\'s Fashion'],
                'gender': 'M',
                'brand': 'Levi\'s',
                'is_featured': False,
            },
            {
                'name': 'Black Leather Jacket',
                'description': 'Premium leather jacket for a stylish look',
                'price': Decimal('199.99'),
                'original_price': Decimal('249.99'),
                'category': categories['Men\'s Fashion'],
                'gender': 'M',
                'brand': 'Zara',
                'is_featured': True,
            },
        ]

        # Create sample products for Women's Fashion
        women_products = [
            {
                'name': 'Elegant Black Dress',
                'description': 'Sophisticated black dress for special occasions',
                'price': Decimal('89.99'),
                'original_price': Decimal('119.99'),
                'category': categories['Women\'s Fashion'],
                'gender': 'W',
                'brand': 'H&M',
                'is_featured': True,
            },
            {
                'name': 'Floral Summer Blouse',
                'description': 'Light and airy blouse perfect for summer',
                'price': Decimal('49.99'),
                'original_price': Decimal('69.99'),
                'category': categories['Women\'s Fashion'],
                'gender': 'W',
                'brand': 'Zara',
                'is_featured': False,
            },
            {
                'name': 'High-Waisted Jeans',
                'description': 'Trendy high-waisted jeans for a modern look',
                'price': Decimal('69.99'),
                'original_price': Decimal('89.99'),
                'category': categories['Women\'s Fashion'],
                'gender': 'W',
                'brand': 'Levi\'s',
                'is_featured': True,
            },
        ]

        # Create sample products for Kids Fashion
        kids_products = [
            {
                'name': 'Colorful Kids T-Shirt',
                'description': 'Fun and comfortable t-shirt for kids',
                'price': Decimal('19.99'),
                'original_price': Decimal('24.99'),
                'category': categories['Kids Fashion'],
                'gender': 'K',
                'brand': 'H&M',
                'is_featured': False,
            },
            {
                'name': 'Kids Denim Shorts',
                'description': 'Durable and comfortable shorts for active kids',
                'price': Decimal('24.99'),
                'original_price': Decimal('34.99'),
                'category': categories['Kids Fashion'],
                'gender': 'K',
                'brand': 'Nike',
                'is_featured': True,
            },
        ]

        # Create accessories (Watches and Sneakers)
        accessories = [
            # Watches
            {
                'name': 'Classic Analog Watch',
                'description': 'Timeless analog watch with leather strap',
                'price': Decimal('149.99'),
                'original_price': Decimal('199.99'),
                'category': categories['Men\'s Fashion'],
                'gender': 'U',
                'brand': 'Gucci',
                'is_accessory': True,
                'accessory_type': 'watch',
                'is_featured': True,
            },
            {
                'name': 'Digital Sports Watch',
                'description': 'High-tech digital watch with fitness tracking',
                'price': Decimal('199.99'),
                'original_price': Decimal('249.99'),
                'category': categories['Men\'s Fashion'],
                'gender': 'U',
                'brand': 'Nike',
                'is_accessory': True,
                'accessory_type': 'watch',
                'is_featured': False,
            },
            {
                'name': 'Elegant Women\'s Watch',
                'description': 'Sophisticated watch perfect for professional women',
                'price': Decimal('179.99'),
                'original_price': Decimal('229.99'),
                'category': categories['Women\'s Fashion'],
                'gender': 'W',
                'brand': 'Prada',
                'is_accessory': True,
                'accessory_type': 'watch',
                'is_featured': True,
            },
            # Sneakers
            {
                'name': 'Comfortable Sneakers',
                'description': 'All-day comfort sneakers for any activity',
                'price': Decimal('89.99'),
                'original_price': Decimal('119.99'),
                'category': categories['Men\'s Fashion'],
                'gender': 'M',
                'brand': 'Adidas',
                'is_accessory': True,
                'accessory_type': 'sneaker',
                'is_featured': True,
            },
            {
                'name': 'Running Sneakers',
                'description': 'High-performance running shoes',
                'price': Decimal('129.99'),
                'original_price': Decimal('159.99'),
                'category': categories['Men\'s Fashion'],
                'gender': 'M',
                'brand': 'Nike',
                'is_accessory': True,
                'accessory_type': 'sneaker',
                'is_featured': False,
            },
            {
                'name': 'Fashion Sneakers',
                'description': 'Stylish sneakers for the modern woman',
                'price': Decimal('99.99'),
                'original_price': Decimal('129.99'),
                'category': categories['Women\'s Fashion'],
                'gender': 'W',
                'brand': 'Adidas',
                'is_accessory': True,
                'accessory_type': 'sneaker',
                'is_featured': True,
            },
            {
                'name': 'Kids Running Shoes',
                'description': 'Comfortable and durable shoes for active kids',
                'price': Decimal('49.99'),
                'original_price': Decimal('69.99'),
                'category': categories['Kids Fashion'],
                'gender': 'K',
                'brand': 'Nike',
                'is_accessory': True,
                'accessory_type': 'sneaker',
                'is_featured': False,
            },
        ]

        # Combine all products
        all_products = men_products + women_products + kids_products + accessories

        # Create products and variants
        for product_data in all_products:
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults=product_data
            )
            
            if created:
                self.stdout.write(f'Created product: {product.name}')
                
                # Create variants for clothing items (not accessories)
                if not product_data.get('is_accessory', False):
                    sizes = ['S', 'M', 'L', 'XL']
                    colors = ['Black', 'White', 'Blue', 'Red']
                    
                    for size in sizes:
                        for color in colors:
                            variant, created = ProductVariant.objects.get_or_create(
                                product=product,
                                size=size,
                                color=color,
                                defaults={
                                    'stock_quantity': 10,
                                    'is_active': True
                                }
                            )
                            if created:
                                self.stdout.write(f'  Created variant: {size} - {color}')
                else:
                    # For accessories, create variants with different colors
                    colors = ['Black', 'White', 'Brown', 'Blue']
                    for color in colors:
                        variant, created = ProductVariant.objects.get_or_create(
                            product=product,
                            size='One Size',
                            color=color,
                            defaults={
                                'stock_quantity': 5,
                                'is_active': True
                            }
                        )
                        if created:
                            self.stdout.write(f'  Created variant: {color}')

        self.stdout.write(
            self.style.SUCCESS('Successfully populated categories and products!')
        )

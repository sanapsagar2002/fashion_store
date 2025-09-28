from django.core.management.base import BaseCommand
from products.models import OutfitRecommendation, OutfitItem, Product, Category
from django.utils import timezone
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Populate database with sample outfit recommendations'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample outfit recommendations...')
        
        # Get existing products
        products = Product.objects.filter(is_active=True)
        if not products.exists():
            self.stdout.write('No products found. Please run populate_sample_data first.')
            return
        
        # Create outfit recommendations
        outfits_data = [
            {
                'name': 'Casual Weekend Look',
                'description': 'Perfect for a relaxed weekend outing with friends or family.',
                'occasion': 'casual',
                'season': 'spring',
                'gender': 'U',
                'items': ['T-Shirts', 'Jeans', 'Shoes']
            },
            {
                'name': 'Business Professional',
                'description': 'Sharp and professional look for office meetings and presentations.',
                'occasion': 'business',
                'season': 'spring',
                'gender': 'U',
                'items': ['Dresses', 'Shoes', 'Accessories']
            },
            {
                'name': 'Summer Date Night',
                'description': 'Elegant and romantic outfit for a special evening out.',
                'occasion': 'date',
                'season': 'summer',
                'gender': 'W',
                'items': ['Dresses', 'Shoes', 'Accessories']
            },
            {
                'name': 'Winter Warmth',
                'description': 'Cozy and warm outfit perfect for cold winter days.',
                'occasion': 'casual',
                'season': 'winter',
                'gender': 'U',
                'items': ['T-Shirts', 'Jeans', 'Shoes', 'Accessories']
            },
            {
                'name': 'Party Ready',
                'description': 'Stylish and trendy outfit for parties and social events.',
                'occasion': 'party',
                'season': 'summer',
                'gender': 'U',
                'items': ['Dresses', 'Shoes', 'Accessories']
            },
            {
                'name': 'Formal Occasion',
                'description': 'Sophisticated and elegant outfit for formal events.',
                'occasion': 'formal',
                'season': 'spring',
                'gender': 'U',
                'items': ['Dresses', 'Shoes', 'Accessories']
            },
            {
                'name': 'Travel Comfort',
                'description': 'Comfortable and practical outfit for long journeys.',
                'occasion': 'travel',
                'season': 'spring',
                'gender': 'U',
                'items': ['T-Shirts', 'Jeans', 'Shoes']
            },
            {
                'name': 'Workout Ready',
                'description': 'Active and comfortable outfit for exercise and fitness.',
                'occasion': 'workout',
                'season': 'summer',
                'gender': 'U',
                'items': ['T-Shirts', 'Shoes']
            }
        ]
        
        for outfit_data in outfits_data:
            outfit, created = OutfitRecommendation.objects.get_or_create(
                name=outfit_data['name'],
                defaults={
                    'description': outfit_data['description'],
                    'occasion': outfit_data['occasion'],
                    'season': outfit_data['season'],
                    'gender': outfit_data['gender']
                }
            )
            
            if created:
                self.stdout.write(f'Created outfit: {outfit.name}')
                
                # Add items to outfit
                item_types = ['top', 'bottom', 'shoes', 'accessory']
                item_index = 0
                
                for category_name in outfit_data['items']:
                    try:
                        category = Category.objects.get(name=category_name)
                        category_products = products.filter(category=category, gender__in=[outfit.gender, 'U'])
                        
                        if category_products.exists():
                            # Select a random product from the category
                            product = category_products.first()
                            
                            OutfitItem.objects.create(
                                outfit=outfit,
                                product=product,
                                item_type=item_types[item_index] if item_index < len(item_types) else 'accessory',
                                is_essential=(item_index < 2)
                            )
                            
                            self.stdout.write(f'  Added {product.name} as {item_types[item_index] if item_index < len(item_types) else "accessory"}')
                            item_index += 1
                        else:
                            self.stdout.write(f'  No products found for category: {category_name}')
                            
                    except Category.DoesNotExist:
                        self.stdout.write(f'  Category not found: {category_name}')
                        continue
                
                # If we don't have enough items, add some accessories
                while item_index < 2 and products.filter(category__name='Accessories').exists():
                    accessory = products.filter(category__name='Accessories').first()
                    OutfitItem.objects.create(
                        outfit=outfit,
                        product=accessory,
                        item_type='accessory',
                        is_essential=True
                    )
                    self.stdout.write(f'  Added accessory: {accessory.name}')
                    item_index += 1
            else:
                self.stdout.write(f'Outfit already exists: {outfit.name}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with outfit recommendations!')
        )

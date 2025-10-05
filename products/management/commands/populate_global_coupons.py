from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from products.models import GlobalDiscountCoupon


class Command(BaseCommand):
    help = 'Populate global discount coupons'

    def handle(self, *args, **options):
        # Clear existing coupons
        GlobalDiscountCoupon.objects.all().delete()
        
        # Create sample global discount coupons
        coupons = [
            {
                'code': 'DISCOUNT10',
                'description': '10% off on all orders',
                'discount_type': 'percentage',
                'discount_value': 10,
                'minimum_order_amount': 50,
                'maximum_discount_amount': 100,
                'maximum_uses': 1000,
                'valid_from': timezone.now(),
                'valid_until': timezone.now() + timedelta(days=365),
            },
            {
                'code': 'DISCOUNT20',
                'description': '20% off on orders over $100',
                'discount_type': 'percentage',
                'discount_value': 20,
                'minimum_order_amount': 100,
                'maximum_discount_amount': 200,
                'maximum_uses': 500,
                'valid_from': timezone.now(),
                'valid_until': timezone.now() + timedelta(days=365),
            },
            {
                'code': 'SAVE50',
                'description': '$50 off on orders over $200',
                'discount_type': 'fixed',
                'discount_value': 50,
                'minimum_order_amount': 200,
                'maximum_uses': 200,
                'valid_from': timezone.now(),
                'valid_until': timezone.now() + timedelta(days=365),
            },
            {
                'code': 'WELCOME',
                'description': '15% off for new customers',
                'discount_type': 'percentage',
                'discount_value': 15,
                'minimum_order_amount': 30,
                'maximum_discount_amount': 75,
                'maximum_uses': 1000,
                'valid_from': timezone.now(),
                'valid_until': timezone.now() + timedelta(days=365),
            },
            {
                'code': 'FLASH30',
                'description': '30% off flash sale',
                'discount_type': 'percentage',
                'discount_value': 30,
                'minimum_order_amount': 75,
                'maximum_discount_amount': 150,
                'maximum_uses': 100,
                'valid_from': timezone.now(),
                'valid_until': timezone.now() + timedelta(days=30),
            }
        ]
        
        for coupon_data in coupons:
            GlobalDiscountCoupon.objects.create(**coupon_data)
            self.stdout.write(
                self.style.SUCCESS(f'Created coupon: {coupon_data["code"]}')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {len(coupons)} global discount coupons')
        )

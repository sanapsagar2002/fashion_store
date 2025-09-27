from rest_framework import serializers
from .models import Order, OrderItem, DiscountCode
from products.serializers import ProductVariantSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product_variant = ProductVariantSerializer(read_only=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('order_number', 'created_at', 'updated_at')

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        order = Order.objects.create(**validated_data)
        
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        
        return order


class OrderCreateSerializer(serializers.Serializer):
    shipping_address = serializers.CharField()
    shipping_city = serializers.CharField()
    shipping_state = serializers.CharField()
    shipping_zip = serializers.CharField()
    shipping_country = serializers.CharField()
    billing_address = serializers.CharField(required=False, allow_blank=True)
    billing_city = serializers.CharField(required=False, allow_blank=True)
    billing_state = serializers.CharField(required=False, allow_blank=True)
    billing_zip = serializers.CharField(required=False, allow_blank=True)
    billing_country = serializers.CharField(required=False, allow_blank=True)
    discount_code = serializers.CharField(required=False, allow_blank=True)
    notes = serializers.CharField(required=False, allow_blank=True)

    def validate_discount_code(self, value):
        if value:
            try:
                discount = DiscountCode.objects.get(code=value)
                if not discount.is_valid():
                    raise serializers.ValidationError('Invalid or expired discount code')
            except DiscountCode.DoesNotExist:
                raise serializers.ValidationError('Invalid discount code')
        return value


class DiscountCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = '__all__'
        read_only_fields = ('used_count', 'created_at')

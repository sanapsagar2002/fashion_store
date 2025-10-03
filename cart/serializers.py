from rest_framework import serializers
from .models import Cart, CartItem
from products.serializers import ProductVariantSerializer
from products.models import ProductVariant


class CartItemSerializer(serializers.ModelSerializer):
    product_variant = ProductVariantSerializer(read_only=True)
    product_variant_id = serializers.IntegerField(write_only=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        fields = ('id', 'product_variant', 'product_variant_id', 'quantity', 'total_price', 'created_at')

    def create(self, validated_data):
        product_variant_id = validated_data.pop('product_variant_id')
        product_variant = ProductVariant.objects.get(id=product_variant_id)
        validated_data['product_variant'] = product_variant

        quantity = int(validated_data.get('quantity', 1))

        # Check if item already exists in cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=validated_data['cart'],
            product_variant=product_variant,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return cart_item

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.ReadOnlyField()
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = ('id', 'items', 'total_items', 'total_price', 'created_at', 'updated_at')

    def get_cart_count(self, obj):
        from .models import CartItem
        return CartItem.objects.filter(cart=obj).count()


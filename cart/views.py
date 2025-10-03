from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from products.models import ProductVariant
from orders.models import DiscountCode


class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    """Add item to cart"""
    product_variant_id = request.data.get('product_variant_id')
    quantity = request.data.get('quantity', 1)
    try:
        quantity = int(quantity)
    except Exception:
        return Response({'error': 'quantity must be an integer'}, status=status.HTTP_400_BAD_REQUEST)

    if not product_variant_id:
        return Response({'error': 'product_variant_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        product_variant = ProductVariant.objects.get(id=product_variant_id)
    except ProductVariant.DoesNotExist:
        return Response({'error': 'Product variant not found'}, status=status.HTTP_404_NOT_FOUND)

    if product_variant.stock_quantity < quantity:
        return Response({'error': 'Insufficient stock'}, status=status.HTTP_400_BAD_REQUEST)

    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product_variant=product_variant,
        defaults={'quantity': quantity}
    )

    if not created:
        # Item already exists - just update quantity, don't increment count
        new_quantity = cart_item.quantity + quantity
        if new_quantity > product_variant.stock_quantity:
            return Response({'error': 'Exceeds available stock'}, status=status.HTTP_400_BAD_REQUEST)
        cart_item.quantity = new_quantity
        cart_item.save()

    serializer = CartItemSerializer(cart_item)
    # Return 201 only for new items, 200 for quantity updates
    return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_cart_item(request, item_id):
    """Update cart item quantity"""
    try:
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
    except CartItem.DoesNotExist:
        return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)

    quantity = request.data.get('quantity')
    if quantity is None:
        return Response({'error': 'quantity is required'}, status=status.HTTP_400_BAD_REQUEST)

    if int(quantity) <= 0:
        cart_item.delete()
        return Response({'message': 'Item removed from cart'}, status=status.HTTP_200_OK)

    try:
        quantity = int(quantity)
    except Exception:
        return Response({'error': 'quantity must be an integer'}, status=status.HTTP_400_BAD_REQUEST)

    if quantity > cart_item.product_variant.stock_quantity:
        return Response({'error': 'Insufficient stock'}, status=status.HTTP_400_BAD_REQUEST)

    cart_item.quantity = quantity
    cart_item.save()

    serializer = CartItemSerializer(cart_item)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    try:
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
    except CartItem.DoesNotExist:
        return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)

    cart_item.delete()
    return Response({'message': 'Item removed from cart'}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def clear_cart(request):
    """Clear all items from cart"""
    try:
        cart = Cart.objects.get(user=request.user)
        cart.items.all().delete()
        return Response({'message': 'Cart cleared'}, status=status.HTTP_200_OK)
    except Cart.DoesNotExist:
        return Response({'message': 'Cart is already empty'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_discount(request):
    """Apply discount code to cart"""
    code = request.data.get('code', '').strip().upper()
    
    if not code:
        return Response({'error': 'Discount code is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        discount = DiscountCode.objects.get(code=code)
    except DiscountCode.DoesNotExist:
        return Response({'error': 'Invalid discount code'}, status=status.HTTP_400_BAD_REQUEST)
    
    if not discount.is_valid():
        return Response({'error': 'Discount code is expired or inactive'}, status=status.HTTP_400_BAD_REQUEST)
    
    cart, _ = Cart.objects.get_or_create(user=request.user)
    
    # Check minimum order amount
    if cart.subtotal < discount.minimum_order_amount:
        return Response({
            'error': f'Minimum order amount of ${discount.minimum_order_amount} required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Calculate discount amount
    if discount.discount_type == 'percentage':
        discount_amount = (cart.subtotal * discount.discount_value) / 100
    else:  # fixed amount
        discount_amount = discount.discount_value
    
    # Apply discount
    cart.discount_code = code
    cart.discount_amount = discount_amount
    cart.save()
    
    return Response({
        'message': f'Discount code "{code}" applied successfully!',
        'discount_amount': float(discount_amount),
        'new_total': float(cart.total_price)
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_discount(request):
    """Apply discount code to cart"""
    try:
        cart = Cart.objects.get(user=request.user)
        code = request.data.get('code')
        
        if not code:
            return Response({'error': 'Discount code is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            discount = DiscountCode.objects.get(code=code, is_active=True)
        except DiscountCode.DoesNotExist:
            return Response({'error': 'Invalid discount code'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if discount is valid
        if not discount.is_valid():
            return Response({'error': 'Discount code has expired'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Calculate discount amount
        subtotal = cart.subtotal
        if discount.discount_type == 'percentage':
            discount_amount = subtotal * (discount.discount_value / 100)
        else:
            discount_amount = min(discount.discount_value, subtotal)
        
        # Apply discount
        cart.discount_code = discount.code
        cart.discount_amount = discount_amount
        cart.save()
        
        return Response({
            'message': 'Discount applied successfully',
            'discount_amount': float(discount_amount),
            'discount_code': discount.code
        }, status=status.HTTP_200_OK)
        
    except Cart.DoesNotExist:
        return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_discount(request):
    """Remove discount code from cart"""
    try:
        cart = Cart.objects.get(user=request.user)
        cart.discount_code = None
        cart.discount_amount = 0
        cart.save()
        return Response({'message': 'Discount removed'}, status=status.HTTP_200_OK)
    except Cart.DoesNotExist:
        return Response({'message': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

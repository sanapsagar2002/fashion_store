from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from decimal import Decimal
from .models import Order, OrderItem, DiscountCode
from .serializers import OrderSerializer, OrderCreateSerializer, DiscountCodeSerializer
from cart.models import Cart, CartItem

class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all().select_related('user').prefetch_related('items')
        return Order.objects.filter(user=self.request.user).select_related('user').prefetch_related('items')

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [IsAuthenticated()]


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def clear_order_history(request):
    try:
        orders = Order.objects.filter(user=request.user)
        deleted_count = orders.count()
        orders.delete()
        return Response({'message': f'{deleted_count} orders deleted successfully.'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order_from_cart(request):
    """Create order from cart items"""
    serializer = OrderCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
        
        if not cart_items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            # Calculate totals
            subtotal = sum(item.total_price for item in cart_items)
            tax_rate = Decimal('0.08')  # 8% tax rate
            tax_amount = subtotal * tax_rate
            shipping_cost = Decimal('0.00') if subtotal >= Decimal('100.00') else Decimal('10.00')  # Free shipping over $100
            
            # Use cart's discount information
            discount_amount = cart.discount_amount or Decimal('0.00')
            discount_code = cart.discount_code
            
            # If discount code is provided in request, validate and apply it
            if serializer.validated_data.get('discount_code') and not discount_code:
                try:
                    discount = DiscountCode.objects.get(code=serializer.validated_data['discount_code'])
                    if discount.is_valid() and subtotal >= discount.minimum_order_amount:
                        if discount.discount_type == 'percentage':
                            discount_amount = (subtotal * discount.discount_value) / Decimal('100')
                        else:
                            discount_amount = Decimal(discount.discount_value)
                        discount_code = discount.code
                        discount.used_count += 1
                        discount.save()
                except DiscountCode.DoesNotExist:
                    pass
            
            total_amount = subtotal + tax_amount + shipping_cost - discount_amount

            # Create order
            order_data = {
                'user': request.user,
                'shipping_address': serializer.validated_data['shipping_address'],
                'shipping_city': serializer.validated_data['shipping_city'],
                'shipping_state': serializer.validated_data['shipping_state'],
                'shipping_zip': serializer.validated_data['shipping_zip'],
                'shipping_country': serializer.validated_data['shipping_country'],
                'billing_address': serializer.validated_data.get('billing_address', ''),
                'billing_city': serializer.validated_data.get('billing_city', ''),
                'billing_state': serializer.validated_data.get('billing_state', ''),
                'billing_zip': serializer.validated_data.get('billing_zip', ''),
                'billing_country': serializer.validated_data.get('billing_country', ''),
                'subtotal': subtotal,
                'tax_amount': tax_amount,
                'shipping_cost': shipping_cost,
                'discount_amount': discount_amount,
                'total_amount': total_amount,
                'notes': serializer.validated_data.get('notes', ''),
            }
            
            order = Order.objects.create(**order_data)

            # Create order items and update stock
            for cart_item in cart_items:
                if cart_item.product_variant.stock_quantity < cart_item.quantity:
                    raise Exception(f'Insufficient stock for {cart_item.product_variant}')
                
                OrderItem.objects.create(
                    order=order,
                    product_variant=cart_item.product_variant,
                    quantity=cart_item.quantity,
                    price=cart_item.product_variant.product.price
                )
                
                # Update stock
                cart_item.product_variant.stock_quantity -= cart_item.quantity
                cart_item.product_variant.save()

            # Clear cart
            cart.items.all().delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    except Cart.DoesNotExist:
        return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_order_status(request, order_id):
    """Update order status (admin only)"""
    order = get_object_or_404(Order, id=order_id)
    
    new_status = request.data.get('status')
    tracking_number = request.data.get('tracking_number', '')
    
    if new_status not in [choice[0] for choice in Order.STATUS_CHOICES]:
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
    
    order.status = new_status
    if tracking_number:
        order.tracking_number = tracking_number
    order.save()
    
    return Response(OrderSerializer(order).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_tracking(request, order_id):
    """Get order tracking information"""
    try:
        if request.user.is_staff:
            order = Order.objects.get(id=order_id)
        else:
            order = Order.objects.get(id=order_id, user=request.user)
        
        return Response(OrderSerializer(order).data)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)


class DiscountCodeListCreateView(generics.ListCreateAPIView):
    queryset = DiscountCode.objects.all()
    serializer_class = DiscountCodeSerializer
    permission_classes = [IsAdminUser]


class DiscountCodeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DiscountCode.objects.all()
    serializer_class = DiscountCodeSerializer
    permission_classes = [IsAdminUser]

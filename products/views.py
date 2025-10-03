from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Category, Product, ProductReview, ProductDiscount, Wishlist
from .serializers import (
    CategorySerializer, 
    ProductSerializer, 
    ProductListSerializer,
    ProductCreateUpdateSerializer,
    ProductReviewSerializer,
    WishlistSerializer
)


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        return [IsAdminUser()]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        return [IsAdminUser()]


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.filter(is_active=True).select_related('category').prefetch_related('images', 'reviews', 'variants')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__name', 'gender', 'brand']
    search_fields = ['name', 'description', 'brand']
    ordering_fields = ['price', 'created_at', 'name']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductListSerializer
        return ProductCreateUpdateSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        return [IsAdminUser()]

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params

        # Map filters
        gender = params.get('gender')
        category_name = params.get('category_name') or params.get('category')
        min_price = params.get('min_price')
        max_price = params.get('max_price')
        size = params.get('size')
        color = params.get('color')
        q = params.get('q')

        if gender:
            queryset = queryset.filter(gender=gender)

        if category_name:
            # Support filtering by category display name
            queryset = queryset.filter(category__name__icontains=category_name)

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        if size:
            queryset = queryset.filter(variants__size=size)

        if color:
            queryset = queryset.filter(variants__color__icontains=color)

        if q:
            queryset = queryset.filter(
                Q(name__icontains=q) |
                Q(description__icontains=q) |
                Q(brand__icontains=q)
            )

        return queryset.distinct()


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.filter(is_active=True).select_related('category').prefetch_related('images', 'variants', 'reviews')
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        return [IsAdminUser()]


class ProductReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductReviewSerializer
    permission_classes = []  # Allow anonymous users to view reviews

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return ProductReview.objects.filter(product_id=product_id).select_related('user').order_by('-created_at')

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Authentication required to create reviews")
        product_id = self.kwargs['product_id']
        serializer.save(user=self.request.user, product_id=product_id)


@api_view(['GET'])
def product_search(request):
    """Advanced product search with filters"""
    query = request.GET.get('q', '')
    category = request.GET.get('category')
    gender = request.GET.get('gender')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    size = request.GET.get('size')
    color = request.GET.get('color')
    
    queryset = Product.objects.filter(is_active=True).select_related('category').prefetch_related('images', 'variants')
    
    if query:
        queryset = queryset.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(brand__icontains=query)
        )
    
    if category:
        queryset = queryset.filter(category__name__icontains=category)
    
    if gender:
        queryset = queryset.filter(gender=gender)
    
    if min_price:
        queryset = queryset.filter(price__gte=min_price)
    
    if max_price:
        queryset = queryset.filter(price__lte=max_price)
    
    if size:
        queryset = queryset.filter(variants__size=size)
    
    if color:
        queryset = queryset.filter(variants__color__icontains=color)
    
    serializer = ProductListSerializer(queryset.distinct(), many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def trending_products(request):
    """Get trending products based on recent orders and reviews"""
    # This is a simplified version - in production, you'd use more sophisticated algorithms
    trending = Product.objects.filter(is_active=True).select_related('category').prefetch_related('images')[:8]
    serializer = ProductListSerializer(trending, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def category_products(request, category_id):
    """Get products by category"""
    try:
        category = Category.objects.get(id=category_id)
        products = Product.objects.filter(category=category, is_active=True).select_related('category').prefetch_related('images')
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)
    except Category.DoesNotExist:
        return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def product_discounts(request, product_id):
    """Get available discount codes for a specific product"""
    try:
        product = Product.objects.get(id=product_id, is_active=True)
        discounts = ProductDiscount.objects.filter(
            product=product,
            is_active=True
        ).select_related('product')
        
        # Filter valid discounts
        valid_discounts = [d for d in discounts if d.is_valid()]
        
        discount_data = []
        for discount in valid_discounts:
            discount_data.append({
                'id': discount.id,
                'code': discount.code,
                'description': discount.description,
                'discount_type': discount.discount_type,
                'discount_value': float(discount.discount_value),
                'minimum_quantity': discount.minimum_quantity,
                'valid_until': discount.valid_until.isoformat(),
            })
        
        return Response(discount_data)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_product_discount(request, product_id):
    """Apply a product-specific discount code"""
    try:
        product = Product.objects.get(id=product_id, is_active=True)
        code = request.data.get('code', '').strip().upper()
        quantity = int(request.data.get('quantity', 1))
        
        if not code:
            return Response({'error': 'Discount code is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            discount = ProductDiscount.objects.get(
                product=product,
                code=code,
                is_active=True
            )
        except ProductDiscount.DoesNotExist:
            return Response({'error': 'Invalid discount code for this product'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not discount.can_be_used(quantity):
            return Response({'error': 'Discount code cannot be used with this quantity or is expired'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Calculate discount amount
        if discount.discount_type == 'percentage':
            discount_amount = (product.price * discount.discount_value) / 100
        else:  # fixed amount
            discount_amount = discount.discount_value
        
        # Update usage count
        discount.used_count += 1
        discount.save()
        
        return Response({
            'message': f'Discount code "{code}" applied successfully!',
            'discount_amount': float(discount_amount),
            'discounted_price': float(product.price - discount_amount),
            'savings': float(discount_amount)
        }, status=status.HTTP_200_OK)
        
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        return Response({'error': 'Invalid quantity'}, status=status.HTTP_400_BAD_REQUEST)


class WishlistListView(generics.ListAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user).select_related('product', 'product__category').prefetch_related('product__images')


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def toggle_wishlist(request, product_id):
    """Add or remove product from wishlist"""
    try:
        product = Product.objects.get(id=product_id, is_active=True)
        
        if request.method == 'POST':
            # Add to wishlist
            wishlist_item, created = Wishlist.objects.get_or_create(
                user=request.user,
                product=product
            )
            if created:
                return Response({'message': 'Product added to wishlist!'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'Product already in wishlist'}, status=status.HTTP_200_OK)
        
        elif request.method == 'DELETE':
            # Remove from wishlist
            try:
                wishlist_item = Wishlist.objects.get(user=request.user, product=product)
                wishlist_item.delete()
                return Response({'message': 'Product removed from wishlist'}, status=status.HTTP_200_OK)
            except Wishlist.DoesNotExist:
                return Response({'error': 'Product not in wishlist'}, status=status.HTTP_404_NOT_FOUND)
                
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Category, Product, ProductReview
from .serializers import (
    CategorySerializer, 
    ProductSerializer, 
    ProductListSerializer,
    ProductCreateUpdateSerializer,
    ProductReviewSerializer
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
    queryset = Product.objects.filter(is_active=True).select_related('category').prefetch_related('images', 'reviews')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'gender', 'brand']
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


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.filter(is_active=True).select_related('category').prefetch_related('images', 'variants', 'reviews')
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return []
        return [IsAdminUser()]


class ProductReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return ProductReview.objects.filter(product_id=product_id).select_related('user')

    def perform_create(self, serializer):
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

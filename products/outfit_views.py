from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.db.models import Q, F
from django.db import transaction
from .models import OutfitRecommendation, OutfitItem, UserOutfitPreference, Product, ProductVariant
from .serializers import (
    OutfitRecommendationSerializer,
    OutfitItemSerializer,
    UserOutfitPreferenceSerializer,
    PersonalizedOutfitSerializer
)


class OutfitRecommendationListView(generics.ListAPIView):
    """Get all outfit recommendations with optional filters"""
    queryset = OutfitRecommendation.objects.filter(is_active=True).prefetch_related('items__product__images')
    serializer_class = OutfitRecommendationSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by occasion
        occasion = self.request.query_params.get('occasion')
        if occasion:
            queryset = queryset.filter(occasion=occasion)
        
        # Filter by season
        season = self.request.query_params.get('season')
        if season:
            queryset = queryset.filter(season=season)
        
        # Filter by gender
        gender = self.request.query_params.get('gender')
        if gender:
            queryset = queryset.filter(gender=gender)
        
        return queryset


class OutfitRecommendationDetailView(generics.RetrieveAPIView):
    """Get detailed outfit recommendation with all items"""
    queryset = OutfitRecommendation.objects.filter(is_active=True).prefetch_related('items__product__images', 'items__product__variants')
    serializer_class = OutfitRecommendationSerializer
    permission_classes = [AllowAny]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_personalized_outfits(request):
    """Get personalized outfit recommendations based on user preferences"""
    try:
        # Get user preferences
        preferences = UserOutfitPreference.objects.filter(user=request.user)
        
        if not preferences.exists():
            # Return general recommendations if no preferences set
            outfits = OutfitRecommendation.objects.filter(is_active=True)[:6]
            serializer = OutfitRecommendationSerializer(outfits, many=True, context={'request': request})
            return Response(serializer.data)
        
        # Build query based on preferences
        outfit_queries = []
        for pref in preferences:
            query = Q(occasion=pref.occasion, season=pref.season, is_active=True)
            outfit_queries.append(query)
        
        # Combine all queries with OR
        combined_query = outfit_queries[0]
        for query in outfit_queries[1:]:
            combined_query |= query
        
        outfits = OutfitRecommendation.objects.filter(combined_query).prefetch_related('items__product__images')
        
        # Apply budget filters if specified
        budget_filtered_outfits = []
        for outfit in outfits:
            total_price = sum(item.product.price for item in outfit.items.all())
            
            # Check if outfit fits any preference budget
            fits_budget = True
            for pref in preferences:
                if (pref.budget_min and total_price < pref.budget_min) or \
                   (pref.budget_max and total_price > pref.budget_max):
                    fits_budget = False
                    break
            
            if fits_budget:
                budget_filtered_outfits.append(outfit)
        
        serializer = OutfitRecommendationSerializer(budget_filtered_outfits[:12], many=True, context={'request': request})
        return Response(serializer.data)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_outfit_from_selection(request):
    """Create a custom outfit from selected products"""
    try:
        product_ids = request.data.get('product_ids', [])
        occasion = request.data.get('occasion', 'casual')
        season = request.data.get('season', 'spring')
        name = request.data.get('name', 'Custom Outfit')
        
        if not product_ids:
            return Response({'error': 'No products selected'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get products
        products = Product.objects.filter(id__in=product_ids, is_active=True)
        if len(products) != len(product_ids):
            return Response({'error': 'Some products not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create outfit recommendation
        with transaction.atomic():
            outfit = OutfitRecommendation.objects.create(
                name=name,
                description=f"Custom outfit created by {request.user.email}",
                occasion=occasion,
                season=season,
                gender=request.data.get('gender', 'U')
            )
            
            # Add items to outfit
            item_types = ['top', 'bottom', 'shoes', 'accessory']
            for i, product in enumerate(products):
                OutfitItem.objects.create(
                    outfit=outfit,
                    product=product,
                    item_type=item_types[i] if i < len(item_types) else 'accessory',
                    is_essential=(i < 2)  # First two items are essential
                )
        
        serializer = OutfitRecommendationSerializer(outfit, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_outfit_suggestions(request):
    """Get outfit suggestions based on a single product"""
    try:
        product_id = request.GET.get('product_id')
        if not product_id:
            return Response({'error': 'Product ID required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            base_product = Product.objects.get(id=product_id, is_active=True)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Find complementary products
        suggestions = []
        
        # Get products from same category or complementary categories
        if base_product.category.name.lower() in ['tops', 'shirts', 't-shirts']:
            # Suggest bottoms
            bottoms = Product.objects.filter(
                category__name__in=['Jeans', 'Pants', 'Shorts', 'Skirts'],
                gender__in=[base_product.gender, 'U'],
                is_active=True
            ).exclude(id=product_id)[:3]
            suggestions.extend(bottoms)
            
            # Suggest shoes
            shoes = Product.objects.filter(
                category__name__in=['Shoes', 'Sneakers'],
                gender__in=[base_product.gender, 'U'],
                is_active=True
            ).exclude(id=product_id)[:2]
            suggestions.extend(shoes)
        
        elif base_product.category.name.lower() in ['jeans', 'pants', 'shorts']:
            # Suggest tops
            tops = Product.objects.filter(
                category__name__in=['T-Shirts', 'Shirts', 'Tops'],
                gender__in=[base_product.gender, 'U'],
                is_active=True
            ).exclude(id=product_id)[:3]
            suggestions.extend(tops)
        
        # Get accessories
        accessories = Product.objects.filter(
            category__name='Accessories',
            gender__in=[base_product.gender, 'U'],
            is_active=True
        ).exclude(id=product_id)[:2]
        suggestions.extend(accessories)
        
        # Remove duplicates
        unique_suggestions = list({product.id: product for product in suggestions}.values())
        
        serializer = PersonalizedOutfitSerializer(unique_suggestions[:6], many=True, context={'request': request})
        return Response(serializer.data)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserOutfitPreferenceView(generics.ListCreateAPIView):
    """Manage user outfit preferences"""
    serializer_class = UserOutfitPreferenceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserOutfitPreference.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_occasion_outfits(request):
    """Get outfit recommendations for specific occasions"""
    occasion = request.GET.get('occasion', 'casual')
    season = request.GET.get('season', 'spring')
    gender = request.GET.get('gender', 'U')
    
    outfits = OutfitRecommendation.objects.filter(
        occasion=occasion,
        season=season,
        gender__in=[gender, 'U'],
        is_active=True
    ).prefetch_related('items__product__images')[:6]
    
    serializer = OutfitRecommendationSerializer(outfits, many=True, context={'request': request})
    return Response(serializer.data)

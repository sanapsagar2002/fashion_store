from django.urls import path
from . import views, outfit_views

urlpatterns = [
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('', views.ProductListCreateView.as_view(), name='product-list-create'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('<int:product_id>/reviews/', views.ProductReviewListCreateView.as_view(), name='product-reviews'),
    path('search/', views.product_search, name='product-search'),
    path('trending/', views.trending_products, name='trending-products'),
    path('category/<int:category_id>/', views.category_products, name='category-products'),
    
    # Outfit Recommendation URLs
    path('outfits/', outfit_views.OutfitRecommendationListView.as_view(), name='outfit-list'),
    path('outfits/<int:pk>/', outfit_views.OutfitRecommendationDetailView.as_view(), name='outfit-detail'),
    path('outfits/personalized/', outfit_views.get_personalized_outfits, name='personalized-outfits'),
    path('outfits/create/', outfit_views.create_outfit_from_selection, name='create-outfit'),
    path('outfits/suggestions/', outfit_views.get_outfit_suggestions, name='outfit-suggestions'),
    path('outfits/occasion/', outfit_views.get_occasion_outfits, name='occasion-outfits'),
    path('outfits/preferences/', outfit_views.UserOutfitPreferenceView.as_view(), name='outfit-preferences'),
]

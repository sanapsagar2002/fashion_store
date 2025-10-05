from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('', views.ProductListCreateView.as_view(), name='product-list-create'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('<int:product_id>/reviews/', views.ProductReviewListCreateView.as_view(), name='product-reviews'),
    path('search/', views.product_search, name='product-search'),
    path('trending/', views.trending_products, name='trending-products'),
    path('category/<int:category_id>/', views.category_products, name='category-products'),
    path('<int:product_id>/discounts/', views.product_discounts, name='product-discounts'),
    path('<int:product_id>/apply-discount/', views.apply_product_discount, name='apply-product-discount'),
    path('wishlist/', views.WishlistListView.as_view(), name='wishlist-list'),
    path('<int:product_id>/wishlist/', views.toggle_wishlist, name='toggle-wishlist'),
    path('global-coupons/', views.global_discount_coupons, name='global-discount-coupons'),
    path('apply-global-discount/', views.apply_global_discount, name='apply-global-discount'),
    path('validate-global-discount/', views.validate_global_discount, name='validate-global-discount'),
]

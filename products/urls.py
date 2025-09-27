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
]

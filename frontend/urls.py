from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('new-collection/', views.new_collection, name='new_collection'),
    path('men-fashion/', views.men_fashion, name='men_fashion'),
    path('women-fashion/', views.women_fashion, name='women_fashion'),
    path('kids-collection/', views.kids_collection, name='kids_collection'),
    path('products/', views.products, name='products'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.orders, name='orders'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<str:token>/', views.reset_password, name='reset_password'),
    path('profile/', views.profile, name='profile'),
    path('wishlist/', views.wishlist, name='wishlist'),
]

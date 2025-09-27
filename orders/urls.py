from django.urls import path
from . import views

urlpatterns = [
    path('', views.OrderListCreateView.as_view(), name='order-list-create'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('create-from-cart/', views.create_order_from_cart, name='create-order-from-cart'),
    path('<int:order_id>/update-status/', views.update_order_status, name='update-order-status'),
    path('<int:order_id>/tracking/', views.order_tracking, name='order-tracking'),
    path('discount-codes/', views.DiscountCodeListCreateView.as_view(), name='discount-code-list'),
    path('discount-codes/<int:pk>/', views.DiscountCodeDetailView.as_view(), name='discount-code-detail'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('check/<str:pincode>/', views.check_delivery, name='check-delivery'),
    path('zones/', views.delivery_zones, name='delivery-zones'),
]

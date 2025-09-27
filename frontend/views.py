from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def home(request):
    return render(request, 'frontend/home.html')


def products(request):
    return render(request, 'frontend/products.html')


def product_detail(request, product_id):
    return render(request, 'frontend/product_detail.html', {'product_id': product_id})


def cart(request):
    return render(request, 'frontend/cart.html')


def checkout(request):
    return render(request, 'frontend/checkout.html')


def orders(request):
    return render(request, 'frontend/orders.html')


def login(request):
    return render(request, 'frontend/login.html')


def register(request):
    return render(request, 'frontend/register.html')


def forgot_password(request):
    return render(request, 'frontend/forgot_password.html')


def reset_password(request, token):
    return render(request, 'frontend/reset_password.html', {'token': token})


@login_required
def profile(request):
    return render(request, 'frontend/profile.html')

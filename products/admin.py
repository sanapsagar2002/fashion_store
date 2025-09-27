from django.contrib import admin
from .models import Category, Product, ProductImage, ProductVariant, ProductReview


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'gender', 'brand', 'is_active', 'created_at')
    list_filter = ('category', 'gender', 'brand', 'is_active', 'created_at')
    search_fields = ('name', 'description', 'brand')
    ordering = ('-created_at',)
    inlines = [ProductImageInline, ProductVariantInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'is_primary', 'created_at')
    list_filter = ('is_primary', 'created_at')
    search_fields = ('product__name',)


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'color', 'stock_quantity', 'sku', 'is_active')
    list_filter = ('size', 'color', 'is_active', 'created_at')
    search_fields = ('product__name', 'sku', 'color')
    ordering = ('product', 'size', 'color')


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'title', 'is_verified_purchase', 'created_at')
    list_filter = ('rating', 'is_verified_purchase', 'created_at')
    search_fields = ('product__name', 'user__email', 'title')
    ordering = ('-created_at',)

from django.contrib import admin
from .models import Order, OrderItem, DiscountCode


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('total_price',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'status', 'payment_status', 'total_amount', 'created_at')
    list_filter = ('status', 'payment_status', 'created_at')
    search_fields = ('order_number', 'user__email')
    ordering = ('-created_at',)
    inlines = [OrderItemInline]
    readonly_fields = ('order_number', 'created_at', 'updated_at')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_variant', 'quantity', 'price', 'total_price', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('order__order_number', 'product_variant__product__name')


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'discount_value', 'used_count', 'max_uses', 'is_active', 'valid_until')
    list_filter = ('discount_type', 'is_active', 'valid_until')
    search_fields = ('code', 'description')
    ordering = ('-created_at',)

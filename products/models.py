from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    GENDER_CHOICES = [
        ('M', 'Men'),
        ('W', 'Women'),
        ('K', 'Kids'),
        ('U', 'Unisex'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='U')
    brand = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - Image {self.id}"


class ProductVariant(models.Model):
    SIZE_CHOICES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
        ('XXXL', 'Triple Extra Large'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    color = models.CharField(max_length=50)
    stock_quantity = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=100, unique=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['product', 'size', 'color']

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = f"{self.product.id}-{self.size}-{self.color}".replace(' ', '').upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.size} - {self.color}"


class ProductReview(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=RATING_CHOICES)
    title = models.CharField(max_length=200)
    comment = models.TextField()
    is_verified_purchase = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['product', 'user']

    def __str__(self):
        return f"{self.user.email} - {self.product.name} - {self.rating} stars"


class OutfitRecommendation(models.Model):
    OCCASION_CHOICES = [
        ('casual', 'Casual'),
        ('formal', 'Formal'),
        ('business', 'Business'),
        ('party', 'Party'),
        ('date', 'Date Night'),
        ('workout', 'Workout'),
        ('travel', 'Travel'),
        ('wedding', 'Wedding'),
    ]

    SEASON_CHOICES = [
        ('spring', 'Spring'),
        ('summer', 'Summer'),
        ('fall', 'Fall'),
        ('winter', 'Winter'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    occasion = models.CharField(max_length=20, choices=OCCASION_CHOICES)
    season = models.CharField(max_length=20, choices=SEASON_CHOICES)
    gender = models.CharField(max_length=1, choices=Product.GENDER_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.get_occasion_display()}"


class OutfitItem(models.Model):
    outfit = models.ForeignKey(OutfitRecommendation, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    item_type = models.CharField(max_length=50)  # e.g., 'top', 'bottom', 'shoes', 'accessory'
    is_essential = models.BooleanField(default=True)  # Essential items vs optional
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['outfit', 'product']

    def __str__(self):
        return f"{self.outfit.name} - {self.product.name} ({self.item_type})"


class UserOutfitPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='outfit_preferences')
    occasion = models.CharField(max_length=20, choices=OutfitRecommendation.OCCASION_CHOICES)
    season = models.CharField(max_length=20, choices=OutfitRecommendation.SEASON_CHOICES)
    preferred_colors = models.JSONField(default=list, blank=True)
    preferred_brands = models.JSONField(default=list, blank=True)
    budget_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    budget_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'occasion', 'season']

    def __str__(self):
        return f"{self.user.email} - {self.get_occasion_display()} {self.get_season_display()}"
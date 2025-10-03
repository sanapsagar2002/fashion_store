from rest_framework import serializers
from .models import Category, Product, ProductImage, ProductVariant, ProductReview, ProductDiscount, Wishlist
from authentication.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductVariantSerializer(serializers.ModelSerializer):
    # Provide minimal nested product info to support cart UI
    class ProductMinimalSerializer(serializers.ModelSerializer):
        primary_image = serializers.SerializerMethodField()

        class Meta:
            model = Product
            fields = ('id', 'name', 'price', 'primary_image')

        def get_primary_image(self, obj):
            primary_img = obj.images.filter(is_primary=True).first()
            if primary_img:
                request = self.context.get('request')
                if request:
                    return request.build_absolute_uri(primary_img.image.url)
                return primary_img.image.url
            return None

    product = ProductMinimalSerializer(read_only=True)

    class Meta:
        model = ProductVariant
        fields = ('id', 'product', 'size', 'color', 'stock_quantity', 'sku', 'is_active', 'created_at')


class ProductReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = ProductReview
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    reviews = ProductReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0

    def get_total_reviews(self, obj):
        return obj.reviews.count()


class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    primary_image = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'category_name', 'gender', 'brand', 
                 'primary_image', 'average_rating', 'total_reviews', 'created_at')

    def get_primary_image(self, obj):
        primary_img = obj.images.filter(is_primary=True).first()
        if primary_img:
            return self.context['request'].build_absolute_uri(primary_img.image.url)
        return None

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return round(sum(review.rating for review in reviews) / len(reviews), 1)
        return 0

    def get_total_reviews(self, obj):
        return obj.reviews.count()


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, required=False)
    variants = ProductVariantSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        variants_data = validated_data.pop('variants', [])
        
        product = Product.objects.create(**validated_data)
        
        for image_data in images_data:
            ProductImage.objects.create(product=product, **image_data)
        
        for variant_data in variants_data:
            ProductVariant.objects.create(product=product, **variant_data)
        
        return product

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', [])
        variants_data = validated_data.pop('variants', [])
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update images
        if images_data:
            instance.images.all().delete()
            for image_data in images_data:
                ProductImage.objects.create(product=instance, **image_data)
        
        # Update variants
        if variants_data:
            instance.variants.all().delete()
            for variant_data in variants_data:
                ProductVariant.objects.create(product=instance, **variant_data)
        
        return instance


# Wishlist Serializer
class WishlistSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    
    class Meta:
        model = Wishlist
        fields = ['id', 'product', 'created_at']


# Product Discount Serializer
class ProductDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDiscount
        fields = ['id', 'code', 'description', 'discount_type', 'discount_value', 'minimum_quantity', 'maximum_uses', 'used_count', 'is_active', 'valid_from', 'valid_until']
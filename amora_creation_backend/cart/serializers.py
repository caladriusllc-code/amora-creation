from rest_framework import serializers
from .models import ( 
    Coupon, Cart, CartItem, GuestInfo
)
from product.models import (
    Product, Category, Collection, Size, Color, ProductImage,
)

# ==========================================
# 1. SÉRIALISEURS DU CATALOGUE
# ==========================================

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'name', 'slug', 'image']


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['id', 'name']


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'name', 'hex_code']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    collection = CollectionSerializer(read_only=True)
    sizes = SizeSerializer(many=True, read_only=True)
    colors = ColorSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price', 
            'discount_price', 'is_active', 
            'created_at', 'category', 'collection', 'sizes',
            'colors', 'images'
        ]


# ==========================================
# 2. SÉRIALISEUR DE COUPON
# ==========================================

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'code', 'discount_type', 'discount_value', 'active']


# ==========================================
# 3. SÉRIALISEURS DU PANIER (CART & CARTITEM)
# ==========================================

class CartItemSerializer(serializers.ModelSerializer):
    # Pour la lecture : renvoie l'objet produit complet
    product = ProductSerializer(read_only=True)
    # Pour l'écriture : permet de passer l'ID du produit lors de l'ajout au panier
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), 
        source='product', 
        write_only=True
    )
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'unit_price', 'subtotal']
        read_only_fields = ['unit_price']

    def get_subtotal(self, obj):
        return str(obj.get_subtotal())


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    coupon = CouponSerializer(read_only=True)
    total = serializers.SerializerMethodField()
    total_with_discount = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            'id', 'session_key', 'coupon', 'items', 
            'total', 'total_with_discount', 'created_at', 'updated_at'
        ]

    def get_total(self, obj):
        return str(obj.get_total())

    def get_total_with_discount(self, obj):
        return str(obj.get_total_with_discount())


# ==========================================
# 4. SÉRIALISEUR DES INFOS INVITÉ (CHECKOUT)
# ==========================================

class GuestInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestInfo
        fields = ['id', 'email', 'full_name', 'phone_number', 'created_at']
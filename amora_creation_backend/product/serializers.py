from rest_framework import serializers
from .models import Category, Collection, Size, Color, Product, ProductVariant, ProductImage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image']

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'name', 'slug', 'image', 'description', 'is_active', 'is_featured', 'created_at']

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['id', 'name', 'code']

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'name', 'hex_code']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_main', 'order']

class ProductVariantSerializer(serializers.ModelSerializer):
    # On imbrique Size et Color pour avoir les détails (nom, hex_code) directement
    # au lieu d'avoir juste un ID (ex: color: 1 -> color: {id: 1, name: "Rouge", hex_code: "#FF0000"})
    size = SizeSerializer(read_only=True)
    color = ColorSerializer(read_only=True)
    
    # On expose la propriété calculée `active_price` qu'on avait créée dans le modèle
    active_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = ProductVariant
        fields = ['id', 'size', 'color', 'sku', 'stock', 'price_override', 'active_price']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    collection = CollectionSerializer(read_only=True)
    sizes = SizeSerializer(many=True, read_only=True)
    colors = ColorSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    total_stock = serializers.IntegerField(read_only=True)
    is_in_stock = serializers.BooleanField(read_only=True)
    
    # 👇 1. Déclarer le nouveau champ calculé
    discount_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price', 'discount_price',
            'category', 'collection', 'is_active', 'is_featured',
            'meta_title', 'meta_description', 'created_at', 'updated_at',
            'images', 'variants', 'sizes', 'colors', 'stock', 'is_in_stock',
            'discount_percentage', 'total_stock'
        ]

    # 👇 3. Créer la méthode qui calcule la réduction (format get_nomduchamp)
    def get_discount_percentage(self, obj):
        if obj.discount_price and obj.price > 0:
            # Calcul : ((Prix de base - Prix soldé) / Prix de base) * 100
            percentage = ((obj.price - obj.discount_price) / obj.price) * 100
            return int(percentage) # On retourne un entier net (ex: 20 pour 20%)
        return None

class CategoryDetailSerializer(CategorySerializer):
    """
    Category serializer that also returns all active products belonging to the category,
    including their variants, images, and stock info.
    """
    products = ProductSerializer(many=True, read_only=True)

    class Meta(CategorySerializer.Meta):
        fields = CategorySerializer.Meta.fields + ['products']
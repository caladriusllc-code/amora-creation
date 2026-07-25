from django.shortcuts import render
from .models import (
    Category, 
    Collection, 
    Size, 
    Color, 
    Product, 
    ProductVariant,
    ProductImage
)
from rest_framework import viewsets
from .serializers import CategorySerializer, CollectionSerializer, ProductSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint pour récupérer toutes les catégories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CollectionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint pour récupérer les collections actives.
    """
    queryset = Collection.objects.filter(is_active=True)
    serializer_class = CollectionSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint pour récupérer les produits actifs avec leurs images et variantes.
    """
    queryset = Product.objects.filter(is_active=True).select_related(
        'category', 'collection'
    ).prefetch_related(
        'images', 'variants', 'variants__size', 'variants__color'
    )
    serializer_class = ProductSerializer
    lookup_field = 'slug'  # Récupère un produit via son slug (ex: /api/products/robe-d-ete/) au lieu de son ID
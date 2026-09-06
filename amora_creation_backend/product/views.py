from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Category, Collection, Product
from .serializers import CategorySerializer, CollectionSerializer, ProductSerializer, CategoryDetailSerializer
from django.db.models import F


class ProductPagination(PageNumberPagination):
    page_size = 12


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
    queryset = Collection.objects.filter(is_active=True).order_by('-is_featured', '-created_at')
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
    pagination_class = ProductPagination
    lookup_field = 'slug'  # Récupère un produit via son slug (ex: /api/products/robe-d-ete/) au lieu de son ID

    # Enable DRF search on the products endpoint, using the `?search=` query param.
    filter_backends = [filters.SearchFilter]
    # Searchable fields: product name, description, slug and related category/collection names
    search_fields = ['name', 'description', 'slug', 'category__name', 'collection__name']

    @action(detail=False, methods=['get'], url_path='on-sale')
    def on_sale(self, request):
        """
        API endpoint pour récupérer uniquement les produits en solde.
        URL: /api/products/on-sale/
        """
        # 1. On filtre les produits qui ont un discount_price non nul
        sale_products = self.get_queryset().filter(discount_price__isnull=False)
        
        # Optionnel : On peut aussi s'assurer que le prix réduit est bien inférieur au prix de base
        sale_products = sale_products.filter(discount_price__lt=F('price'))

        # 2. Gestion de la pagination (important s'il y a beaucoup de produits en solde)
        page = self.paginate_queryset(sale_products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # 3. Sérialisation et réponse
        serializer = self.get_serializer(sale_products, many=True)
        return Response(serializer.data)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

    @action(detail=True, methods=['get'], url_path='products')
    def products(self, request, slug=None):  # 👈 1. Remplacer pk par slug ici
        """
        Retrieve a single category along with its products via its slug.
        URL: /api/categories/<slug>/products/
        """
        try:
            # 2. Utiliser directement le slug pour la requête avec prefetch_related
            category = Category.objects.prefetch_related(
                'products__images',
                'products__variants',
                'products__variants__size',
                'products__variants__color',
                'products__category',
                'products__collection'
            ).get(slug=slug)  # 👈 3. Faire le get() sur le slug
            
        except Category.DoesNotExist:
            return Response(
                {"detail": "Cette catégorie est introuvable."}, 
                status=404
            )

        serializer = CategoryDetailSerializer(category)
        return Response(serializer.data)
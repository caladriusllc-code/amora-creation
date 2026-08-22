from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, Collection, Product
from .serializers import CategorySerializer, CollectionSerializer, ProductSerializer, CategoryDetailSerializer

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
    lookup_field = 'slug'  # Récupère un produit via son slug (ex: /api/products/robe-d-ete/) au lieu de son ID

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
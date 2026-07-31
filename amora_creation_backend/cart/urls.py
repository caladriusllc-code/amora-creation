from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CartViewSet, 
    GuestInfoViewSet
)

# 1. Initialisation du routeur
router = DefaultRouter()

# 2. Enregistrement de nos ViewSets
# Le premier argument est le chemin dans l'URL (ex: 'products' donnera /products/)
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'checkout', GuestInfoViewSet, basename='checkout')

# 3. Inclusion des URLs générées dans les urlpatterns de l'application
urlpatterns = [
    path('', include(router.urls)),
]
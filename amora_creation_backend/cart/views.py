from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import (
    Product, Coupon, 
    Cart, CartItem, GuestInfo
)
from product.models import(
    Product, Category, Collection,
)
from .serializers import *

class CartViewSet(viewsets.ViewSet):
    """
    Gestion du panier par session_key pour le frontend Nuxt.js.
    """

    def _get_or_create_cart(self, session_key):
        if not session_key:
            return None, False
        cart, created = Cart.objects.get_or_create(session_key=session_key)
        return cart, created

    @action(detail=False, methods=['get'])
    def get_cart(self, request):
        """Récupère le panier en fonction du header X-Session-Key ou paramètre URL."""
        session_key = request.query_params.get('session_key') or request.headers.get('X-Session-Key')
        if not session_key:
            return Response({'error': 'Une clé de session est requise.'}, status=status.HTTP_400_BAD_REQUEST)

        cart, _ = self._get_or_create_cart(session_key)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        """Ajoute un produit au panier."""
        session_key = request.data.get('session_key')
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        if not session_key or not product_id:
            return Response(
                {'error': 'Les champs session_key et product_id sont requis.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        cart, _ = self._get_or_create_cart(session_key)
        product = get_object_or_404(Product, id=product_id)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'unit_price': product.prix, 'quantity': quantity}
        )

        if not created:
            item.quantity += quantity
            item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def update_item_quantity(self, request):
        """Met à jour la quantité d'un article du panier."""
        item_id = request.data.get('item_id')
        quantity = int(request.data.get('quantity', 1))

        item = get_object_or_404(CartItem, id=item_id)
        if quantity > 0:
            item.quantity = quantity
            item.save()
        else:
            item.delete()

        serializer = CartSerializer(item.cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        """Supprime un article du panier."""
        item_id = request.data.get('item_id')
        item = get_object_or_404(CartItem, id=item_id)
        cart = item.cart
        item.delete()

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def apply_coupon(self, request):
        """Applique un code promo au panier."""
        session_key = request.data.get('session_key')
        code = request.data.get('code')

        cart, _ = self._get_or_create_cart(session_key)
        if not cart:
            return Response({'error': 'Panier introuvable.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            coupon = Coupon.objects.get(code__iexact=code)
            if coupon.is_valid():
                cart.coupon = coupon
                cart.save()
                serializer = CartSerializer(cart)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Ce code promo est expiré ou invalide.'}, status=status.HTTP_400_BAD_REQUEST)
        except Coupon.DoesNotExist:
            return Response({'error': 'Code promo introuvable.'}, status=status.HTTP_404_NOT_FOUND)


# ==========================================
# 3. VUE CHECKOUT / GUEST INFO
# ==========================================

class GuestInfoViewSet(viewsets.ModelViewSet):
    """
    Enregistre les coordonnées des clients invités lors de la commande.
    """
    queryset = GuestInfo.objects.all()
    serializer_class = GuestInfoSerializer
    http_method_names = ['post'] # Sécurité : seule la création (POST) est autorisée
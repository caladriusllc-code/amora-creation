import uuid
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import (
    Coupon, Cart, CartItem, GuestInfo
)
from product.models import (
    Product, Category, Collection, Size, Color
)
from .serializers import *

class CartViewSet(viewsets.ViewSet):
    """
    Gestion du panier par Cookies pour le frontend Nuxt.js.
    """

    def _get_or_create_cart(self, request):
        """
        Récupère le panier via le cookie. S'il n'y a pas de cookie, 
        génère un nouvel ID et crée un panier.
        Retourne le panier, l'ID de session, et un booléen indiquant si c'est une nouvelle session.
        """
        session_id = request.COOKIES.get('session_id')
        is_new_session = False

        if not session_id:
            session_id = uuid.uuid4().hex # Génère un identifiant unique (ex: 3b1a...)
            is_new_session = True

        cart, created = Cart.objects.get_or_create(session_key=session_id)
        return cart, session_id, is_new_session

    def _set_cookie_if_needed(self, response, session_id, is_new_session):
        """
        Attache le cookie à la réponse si c'est une nouvelle session.
        """
        if is_new_session:
            response.set_cookie(
                key='session_id',
                value=session_id,
                max_age=30 * 24 * 60 * 60, # Expire dans 30 jours
                samesite='Lax', # Essentiel pour la communication Nuxt <-> Django
                httponly=True,  # Sécurité : Empêche le JavaScript de lire le cookie directement
                # secure=True,  # TODO: Décommenter en production (quand tu seras en HTTPS)
            )
        return response

    @method_decorator(ensure_csrf_cookie)
    @action(detail=False, methods=['get'])
    def get_cart(self, request):
        """Récupère ou crée le panier en fonction du cookie."""
        cart, session_id, is_new = self._get_or_create_cart(request)
        
        serializer = CartSerializer(cart)
        response = Response(serializer.data, status=status.HTTP_200_OK)
        
        return self._set_cookie_if_needed(response, session_id, is_new)

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        """Ajoute un produit au panier avec vérification des stocks."""
        cart, session_id, is_new = self._get_or_create_cart(request)
        
        product_id = request.data.get('product_id')
        # On sécurise la conversion en entier au cas où le frontend enverrait une chaîne
        try:
            quantity = int(request.data.get('quantity', 1))
        except ValueError:
            return Response(
                {'error': 'La quantité doit être un nombre entier.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        size_id = request.data.get('size_id')
        color_id = request.data.get('color_id')

        if not product_id:
            return Response(
                {'error': 'Le champ product_id est requis.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        product = get_object_or_404(Product, id=product_id)
        size = get_object_or_404(Size, id=size_id) if size_id else None
        color = get_object_or_404(Color, id=color_id) if color_id else None

        # ⚡️ 1. Vérification des stocks avant création
        # On cherche si cet article précis est déjà dans le panier
        existing_item = CartItem.objects.filter(
            cart=cart, 
            product=product, 
            size=size, 
            color=color
        ).first()

        # On calcule la quantité totale que l'utilisateur souhaite avoir au final
        total_requested = quantity
        if existing_item:
            total_requested += existing_item.quantity

        # On compare avec le stock absolu du produit principal
        if total_requested > product.stock:
            return Response(
                {'error': f'Stock insuffisant. Il ne reste que {product.stock} exemplaire(s) disponible(s).'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # ⚡️ 2. Ajout ou mise à jour si le stock est validé
        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            size=size,
            color=color,
            defaults={'unit_price': product.price, 'quantity': quantity}
        )

        if not created:
            item.quantity += quantity
            item.save()

        serializer = CartSerializer(cart)
        response = Response(serializer.data, status=status.HTTP_200_OK)
        return self._set_cookie_if_needed(response, session_id, is_new)

    @action(detail=False, methods=['post'])
    def update_item_quantity(self, request):
        """Met à jour la quantité d'un article du panier."""
        # Plus besoin de demander session_key !
        cart, session_id, is_new = self._get_or_create_cart(request)
        
        item_id = request.data.get('item_id')
        quantity = int(request.data.get('quantity', 1))

        # On s'assure que l'item appartient bien au panier actuel par sécurité
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        
        if quantity > 0:
            item.quantity = quantity
            item.save()
        else:
            item.delete()

        serializer = CartSerializer(cart)
        response = Response(serializer.data, status=status.HTTP_200_OK)
        return self._set_cookie_if_needed(response, session_id, is_new)

    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        """Supprime un article du panier."""
        cart, session_id, is_new = self._get_or_create_cart(request)
        
        item_id = request.data.get('item_id')
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        item.delete()

        serializer = CartSerializer(cart)
        response = Response(serializer.data, status=status.HTTP_200_OK)
        return self._set_cookie_if_needed(response, session_id, is_new)

    @action(detail=False, methods=['post'])
    def apply_coupon(self, request):
        """Applique un code promo au panier."""
        cart, session_id, is_new = self._get_or_create_cart(request)
        code = request.data.get('code')

        try:
            coupon = Coupon.objects.get(code__iexact=code)
            if coupon.is_valid():
                cart.coupon = coupon
                cart.save()
                serializer = CartSerializer(cart)
                response = Response(serializer.data, status=status.HTTP_200_OK)
                return self._set_cookie_if_needed(response, session_id, is_new)
            else:
                return Response({'error': 'Ce code promo est expiré ou invalide.'}, status=status.HTTP_400_BAD_REQUEST)
        except Coupon.DoesNotExist:
            return Response({'error': 'Code promo introuvable.'}, status=status.HTTP_404_NOT_FOUND)
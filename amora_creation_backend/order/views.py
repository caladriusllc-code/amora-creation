from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db import transaction

from cart.models import Cart
from order.models import Order, OrderItem, GuestInfo, ShippingZone

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from decimal import Decimal


def get_cart_weight(cart):
    """Retourne les articles pesés et le poids total du panier."""
    items = list(cart.items.select_related('product__weight').all())
    weighted_items = [item for item in items if item.product and item.product.weight]
    total_weight = sum(
        (
            item.product.weight.code * item.quantity
            for item in weighted_items
        ),
        Decimal('0.00')
    )
    return items, weighted_items, total_weight


def get_shipping_rate(zone, cart):
    """Retourne le tarif applicable au panier et son poids calculé."""
    items, weighted_items, total_weight = get_cart_weight(cart)

    if not items or len(weighted_items) == len(items):
        matching_rate = zone.rates.filter(
            min_weight__lte=total_weight,
            max_weight__gte=total_weight,
        ).first()
    else:
        matching_rate = None

    # Until every product has a weight, use the zone's base rate rather than
    # rejecting a valid order with a 0 kg weight.
    if matching_rate is None and items and not weighted_items:
        matching_rate = zone.rates.order_by('min_weight').first()

    return matching_rate, total_weight


@method_decorator(csrf_exempt, name='dispatch')
class OrderViewSet(viewsets.ViewSet):
    """
    Gestion des commandes.
    """

    @action(detail=False, methods=['get'], url_path='shipping-zones', permission_classes=[AllowAny])
    def shipping_zones(self, request):
        """Retourne les zones actives et les tarifs correspondant au panier courant."""
        session_key = (
            request.query_params.get('session_key')
            or request.COOKIES.get('session_id')
            or request.COOKIES.get('session_key')
        )
        total_weight = Decimal('0.00')

        if session_key:
            cart = Cart.objects.filter(session_key=session_key).first()
            if cart:
                _, _, total_weight = get_cart_weight(cart)

        zones = []
        for zone in ShippingZone.objects.filter(is_active=True).prefetch_related('rates'):
            rates = [
                {
                    'min_weight': str(rate.min_weight),
                    'max_weight': str(rate.max_weight),
                    'price': str(rate.price),
                }
                for rate in zone.rates.all()
            ]
            matching_rate, _ = get_shipping_rate(zone, cart) if session_key and cart else (None, total_weight)
            zones.append({
                'id': zone.id,
                'name': zone.name,
                'rates': rates,
                'shipping_fee': str(matching_rate.price if matching_rate else Decimal('0.00')),
            })

        return Response({
            'zones': zones,
            'total_weight': str(total_weight),
        })

    @action(detail=False, methods=['post'])
    @transaction.atomic
    def checkout(self, request):
        """
        Endpoint: POST /api/orders/checkout/
        """
        data = request.data
        session_key = (
            data.get('session_key') 
            or request.COOKIES.get('session_id') 
            or request.COOKIES.get('session_key')
        )

        if not session_key:
            return Response({"error": "Session key manquante."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart = Cart.objects.get(session_key=session_key)
        except Cart.DoesNotExist:
            return Response({"error": "Panier introuvable."}, status=status.HTTP_404_NOT_FOUND)

        if not cart.items.exists():
            return Response({"error": "Votre panier est vide."}, status=status.HTTP_400_BAD_REQUEST)

        email = data.get('email')
        full_name = data.get('full_name')
        phone_number = data.get('phone_number')
        shipping_address = data.get('shipping_address')
        city = data.get('city')
        shipping_zone_id = data.get('shipping_zone')

        if not all([email, full_name, phone_number, shipping_address, city]):
            return Response(
                {"error": "Veuillez remplir toutes les informations de livraison."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        shipping_zone = None
        shipping_fee = Decimal('0.00')
        if shipping_zone_id:
            shipping_zone = ShippingZone.objects.filter(
                id=shipping_zone_id,
                is_active=True,
            ).prefetch_related('rates').first()
            if not shipping_zone:
                return Response(
                    {"error": "La zone de livraison sélectionnée est indisponible."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            matching_rate, _ = get_shipping_rate(shipping_zone, cart)
            if not matching_rate:
                return Response(
                    {"error": "Aucun tarif ne couvre le poids de votre panier pour cette zone."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            shipping_fee = matching_rate.price

        # ⚡️ NOUVEAU 1: Vérification ultime des stocks avant de créer quoi que ce soit
        for item in cart.items.all():
            if item.quantity > item.product.stock:
                return Response(
                    {"error": f"Le produit '{item.product.name}' n'est plus disponible en quantité suffisante (Restant: {item.product.stock})."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

        guest_info = GuestInfo.objects.create(
            email=email,
            full_name=full_name,
            phone_number=phone_number,
            shipping_address=shipping_address,
            city=city
        )

        order = Order.objects.create(
            guest=guest_info,
            status=Order.Status.PENDING,
            coupon=cart.coupon,
            shipping_zone=shipping_zone,
            shipping_fee=shipping_fee,
        )

        if cart.coupon and cart.coupon.is_valid():
            subtotal = cart.get_total() 
            discount_amount = Decimal('0.00')
            
            if cart.coupon.discount_type == 'percentage':
                discount_amount = (cart.coupon.discount_value / Decimal('100')) * subtotal
            elif cart.coupon.discount_type == 'fixed':
                discount_amount = Decimal(str(cart.coupon.discount_value))
            
            order.discount_amount = discount_amount
            cart.coupon.used_count += 1
            cart.coupon.save()

        order.save()

        for item in cart.items.all():
            # Création de la ligne de commande[cite: 3]
            OrderItem.objects.create(
                order=order,
                product=item.product,
                unit_price=item.unit_price,
                quantity=item.quantity
            )
            
            # ⚡️ NOUVEAU 2: Déduction du stock absolu sur le produit
            item.product.stock -= item.quantity
            item.product.save()

        order.update_total()
        
        cart.clear()
        cart.coupon = None
        cart.save()

        return Response({
            "message": "Commande créée avec succès.",
            "id": order.id,
            "order_id": order.id,
            "total_amount": order.total_amount,
            "status": order.status,
        }, status=status.HTTP_201_CREATED)
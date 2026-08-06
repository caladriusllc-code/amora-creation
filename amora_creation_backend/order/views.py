from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db import transaction

from cart.models import Cart
from order.models import Order, OrderItem, GuestInfo

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class OrderViewSet(viewsets.ViewSet):
    """
    Gestion des commandes.
    """
    # 👇 AJOUTE CETTE LIGNE ICI
    authentication_classes = [] 

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    @transaction.atomic
    def checkout(self, request):
        """
        Endpoint: POST /api/orders/checkout/
        """
        data = request.data
        session_key = data.get('session_key')

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

        if not all([email, full_name, phone_number, shipping_address, city]):
            return Response(
                {"error": "Veuillez remplir toutes les informations de livraison."}, 
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
        )

        if cart.coupon and cart.coupon.is_valid():
            subtotal = cart.get_total()
            discount_amount = 0
            
            if cart.coupon.discount_type == 'percentage':
                discount_amount = (cart.coupon.discount_value / 100) * subtotal
            elif cart.coupon.discount_type == 'fixed':
                discount_amount = cart.coupon.discount_value
            
            order.discount_amount = discount_amount
            cart.coupon.used_count += 1
            cart.coupon.save()

        order.save()

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                unit_price=item.unit_price,
                quantity=item.quantity
            )

        order.update_total()
        
        cart.clear()
        cart.coupon = None
        cart.save()

        return Response({
            "message": "Commande créée avec succès.",
            "order_id": order.id,
            "total_amount": order.total_amount
        }, status=status.HTTP_201_CREATED)
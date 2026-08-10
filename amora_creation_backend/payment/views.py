# payment/views.py
import json
import requests  # pip install requests
import zipfile
import io
import tempfile
import os

from django.http    import FileResponse
from django.conf    import settings
from django.shortcuts import get_object_or_404
from django.db.models import F
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)

from rest_framework.views       import APIView
from rest_framework.response    import Response
from rest_framework             import status
from rest_framework.permissions import AllowAny

from order.models import Order
from .models          import Transaction
from .serializers     import (
    TransactionSerializer,
    PaymentInitiateSerializer,
    PaymentSimulateSerializer,
)

# ─────────────────────────────────────────
# INITIATE  —  POST /payment/initiate/
# ─────────────────────────────────────────

class PaymentInitiateView(APIView):
    """
    POST /payment/initiate/
    Crée une Transaction PENDING, appelle l'API sandbox xpaye,
    et retourne l'URL de redirection vers leur page de paiement.
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = PaymentInitiateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        order_id       = serializer.validated_data['order_id']
        payment_method = serializer.validated_data['payment_method']

        # On précharge guest et user pour éviter des requêtes supplémentaires
        order = get_object_or_404(
            Order.objects.select_related('guest', 'user'),
            id=order_id
        )

        if order.status != Order.Status.PENDING:
            return Response(
                {'message': f'Commande non payable (statut : {order.get_status_display()}).'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ── Créer la Transaction — son UUID devient notre referenceNumber ──
        transaction = Transaction.objects.create(
            order              = order,
            amount             = order.total_amount,
            payment_method     = payment_method,
            status             = Transaction.TransactionStatus.PENDING,
            provider_reference = None,
        )
        transaction.provider_reference = str(transaction.id)
        transaction.save(update_fields=['provider_reference'])

        # ── Décomposer le nom (GuestInfo.full_name → first / last) ────────
        if order.guest:
            # GuestInfo.full_name = "Ishola Lamine" → split sur le premier espace
            name_parts = order.guest.full_name.strip().split(' ', 1)
            first_name = name_parts[0]
            last_name  = name_parts[1] if len(name_parts) > 1 else ''
            phone      = order.guest.phone_number   # GuestInfo.phone_number
        else:
            first_name = getattr(order.user, 'first_name', '') or ''
            last_name  = getattr(order.user, 'last_name',  '') or ''
            phone      = getattr(order.user, 'phone_number', '') or ''

        # ── Payload calé sur leur format sandbox ──────────────────────────
        xpaye_payload = {
            'merchantId'         : settings.XPAYE_MERCHANT_ID,
            'amount'             : int(order.total_amount),      # entier FCFA
            'description'        : f'Commande {str(order.id)[:8]}',
            'channel'            : 'CARD',
            'countryCurrencyCode': '952',                        # FCFA XOF
            'referenceNumber'    : str(transaction.id),          # ← notre clé de récup
            'customerEmail'      : order.buyer_email,            # property Order
            'customerFirstName'  : first_name,
            'customerLastname'   : last_name,
            'customerPhoneNumber': phone,
            'notificationURL'    : settings.XPAYE_NOTIFICATION_URL,
            'returnURL'          : settings.XPAYE_RETURN_URL,
            'returnContext'      : json.dumps({'order_id': str(order.id)}),
        }

        # ── Appel API sandbox xpaye ───────────────────────────────────────
        try:
            xpaye_resp = requests.post(
                settings.XPAYE_API_URL,
                json    = xpaye_payload,
                timeout = 15,
            )
            # 💡 ASTUCE DEBUG : Affiche la réponse brute de la sandbox dans ton terminal Django
            print(f"--- STATUS XPAYE : {xpaye_resp.status_code} ---")
            print(f"--- REPONSE XPAYE : {xpaye_resp.text} ---")
            xpaye_resp.raise_for_status()
            xpaye_data = xpaye_resp.json()
        except requests.RequestException as e:
            # Transaction reste PENDING → l'utilisateur peut réessayer
            return Response(
                {'message': 'Erreur de connexion à xpaye.', 'error': str(e)},
                status=status.HTTP_502_BAD_GATEWAY
            )

        # ── Réponse xpaye : {"success": true, "message": "...", "url": "..."} ──
        if not xpaye_data.get('success'):
            # xpaye a répondu mais avec un échec applicatif
            transaction.status        = Transaction.TransactionStatus.FAILED
            transaction.error_message = xpaye_data.get('message', 'Échec retourné par xpaye.')
            transaction.save(update_fields=['status', 'error_message'])

            return Response(
                {'message': xpaye_data.get('message', 'Paiement non initialisé.')},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ── Succès → retourner l'URL au frontend pour redirection ─────────
        return Response(
            {
                'data'       : TransactionSerializer(transaction).data,
                'payment_url': xpaye_data.get('url'),   # "https://sandbox.paiementpro.net/..."
                'message'    : xpaye_data.get('message', 'Initialisation réussie.'),
            },
            status=status.HTTP_201_CREATED
        )

# ─────────────────────────────────────────
# SIMULATE  —  POST /payment/simulate/
# (sandbox / DEBUG uniquement)
# ─────────────────────────────────────────

class PaymentSimulateView(APIView):
    """
    Simule un retour xpaye sans appeler leur API.
    Désactivé automatiquement hors DEBUG.
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        if not settings.DEBUG:
            return Response(
                {'message': 'Endpoint non disponible en production.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = PaymentSimulateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        transaction_id = serializer.validated_data['transaction_id']
        outcome        = serializer.validated_data['outcome']   # 'SUCCESS' ou 'FAILED'

        transaction = get_object_or_404(
            Transaction.objects.select_related('order__guest', 'order__user'),
            id=transaction_id
        )

        if transaction.status != Transaction.TransactionStatus.PENDING:
            return Response(
                {'message': f'Transaction déjà traitée ({transaction.get_status_display()}).'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if outcome == 'SUCCESS':
            transaction.status = Transaction.TransactionStatus.SUCCESSFUL
            transaction.save()

            order        = transaction.order
            order.status = Order.Status.PAID
            order.save()

        else:
            transaction.status        = Transaction.TransactionStatus.FAILED
            transaction.error_message = 'Échec simulé manuellement (sandbox).'
            transaction.save()

        return Response(
            {
                'data'   : TransactionSerializer(transaction).data,
                'message': f'Simulation terminée : {outcome}.',
            },
            status=status.HTTP_200_OK
        )


# ─────────────────────────────────────────
# WEBHOOK  —  POST /payment/webhook/
# ─────────────────────────────────────────

@csrf_exempt
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def payment_webhook_view(request):
    """
    Reçoit la notification xpaye après paiement.
    Met à jour la transaction, la commande, et envoie l'email.
    On répond TOUJOURS 200 pour éviter les réessais intempestifs de xpaye.
    """
    try:
        data = request.data if request.data else json.loads(request.body)
    except json.JSONDecodeError:
        return Response({'message': 'Payload JSON invalide.'}, status=status.HTTP_200_OK)

    #print("Webhook reçu :", data)

    reference      = data.get('referenceNumber')
    response_code  = data.get('responsecode')
    pay_status     = data.get('status')
    success_flag   = data.get('success')
    error_msg      = data.get('message', '')

    # XPAYE peut envoyer un code numérique (0 = succès) ou un statut texte.
    is_success = (
        str(response_code) == '0'
        or str(pay_status).upper() in {'SUCCESS', 'SUCCEEDED', 'PAID', 'OK'}
        or str(success_flag).upper() in {'TRUE', '1', 'SUCCESS', 'SUCCEEDED'}
    )

    if not reference:
        return Response({'message': 'referenceNumber manquant.'}, status=status.HTTP_200_OK)

    try:
        transaction = Transaction.objects.select_related(
            'order__guest', 'order__user'
        ).get(provider_reference=reference)
    except Transaction.DoesNotExist:
        return Response({'message': 'Transaction inconnue.'}, status=status.HTTP_200_OK)

    # Idempotence
    if transaction.status != Transaction.TransactionStatus.PENDING:
        return Response({'message': 'Déjà traité.'}, status=status.HTTP_200_OK)

    if is_success:
        transaction.status = Transaction.TransactionStatus.SUCCESSFUL
        transaction.error_message = None
        transaction.save(update_fields=['status', 'error_message'])

        order = transaction.order
        order.status = Order.Status.PAID
        order.save(update_fields=['status'])

        return Response(
            {'message': 'Paiement confirmé — téléchargement prêt.'},
            status=status.HTTP_200_OK
        )

    transaction.status = Transaction.TransactionStatus.FAILED
    transaction.error_message = error_msg or (
        f"Échec du paiement (responsecode={response_code})."
    )
    transaction.save(update_fields=['status', 'error_message'])

    return Response(
        {'message': 'Paiement échoué.'},
        status=status.HTTP_200_OK
    )


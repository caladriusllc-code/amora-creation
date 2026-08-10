from django.db import models
# Remplace 'ecommerce' par le vrai nom de l'application où se trouve ton modèle Order
from order.models import Order 
import uuid

class Transaction(models.Model):
    
    class TransactionStatus(models.TextChoices):
        PENDING = 'PENDING', 'En attente'
        SUCCESSFUL = 'SUCCESSFUL', 'Réussie'
        FAILED = 'FAILED', 'Échouée'
        CANCELED = 'CANCELED', 'Annulée'

    class PaymentMethod(models.TextChoices):
        STRIPE = 'STRIPE', 'Stripe'
        CINETPAY = 'CINETPAY', 'CinetPay'
        WAVE = 'WAVE', 'Wave'
        ORANGE_CI='OMCIV2'
        MOOV_CI='FLOOZ'
        MTN_CI='MOMOCI'
        ORANGE_BF='OMBF'
        ORANGE_MALI='OMML'
        MTN_BENIN='MOMOBJ'
        VISA_MASTERCARD='CARD'
        MOOV_BENIN='FLOOZBJ'
        AIRTEL_NIGER='AIRTELNG'
        WAVE_CI='WAVECI'
        ORANGE_SENEGAL='OMSN'
        ORANGE_GUINEE_BISSAU='OMGN'
        ORANGE_CAMEROUN='OMCM'
        WAVE_SENEGAL='WAVESN'
        FLOOZ_TOGO='MOOTG'
        TOGO_CEL='TOGOCEL'
        MTN_CAMEROUN='MOMOCM'
        PAYPAL = 'PAYPAL', 'PayPal',
        SIMULATION = 'SIMULATED', 'Simulation'  # Pour les tests en dev
        # N'hésite pas à adapter cette liste selon tes prestataires africains ou internationaux

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


    # 1. Le lien avec la commande
    # On utilise ForeignKey et non OneToOne car un client peut rater un paiement 
    # (ex: erreur de carte) et réessayer. Une commande peut donc avoir plusieurs transactions.
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name='transactions'
    )
    
    # 2. La référence du prestataire (Crucial !)
    # C'est l'ID unique que Stripe, PayPal ou CinetPay va te renvoyer. 
    # C'est grâce à ce champ que ton Webhook retrouvera la transaction.
    provider_reference = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        unique=True,
        help_text="ID de la transaction généré par le prestataire de paiement"
    )

    # 3. Les informations financières
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Montant exact tenté lors de cette transaction"
    )
    
    status = models.CharField(
        max_length=20, 
        choices=TransactionStatus.choices, 
        default=TransactionStatus.PENDING
    )
    
    payment_method = models.CharField(
        max_length=20, 
        choices=PaymentMethod.choices,
        default=PaymentMethod.STRIPE
    )

    # 4. Le suivi des erreurs
    # Très utile pour le support client si un utilisateur se plaint que son paiement ne passe pas
    error_message = models.TextField(
        blank=True, 
        null=True,
        help_text="Message d'erreur renvoyé par la banque en cas d'échec"
    )

    # 5. Les dates de traçabilité
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

    def __str__(self):
        return f"Transaction {self.id} | Cmd: {self.order.id} | {self.amount}FCFA | {self.get_status_display()}"
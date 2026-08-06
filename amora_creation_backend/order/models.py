import uuid
from django.db import models
from django.conf import settings
from product.models import Product
from cart.models import Coupon # Assure-toi que l'import correspond à ton architecture

class GuestInfo(models.Model):
    """
    Infos de l'invité collectées au checkout.
    Lié à la commande (Order) — pas au panier.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField()
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)
    
    # Pour un e-commerce physique (vêtements), l'adresse de livraison est cruciale
    shipping_address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.email})"

class Order(models.Model):

    class Status(models.TextChoices):
        PENDING   = 'pending',   'En attente de paiement'
        PAID      = 'paid',      'Payé'
        SHIPPED   = 'shipped',   'Expédié'
        DELIVERED = 'delivered', 'Livré'
        CANCELLED = 'cancelled', 'Annulé'
        REFUNDED  = 'refunded',  'Remboursé'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Relation vers un utilisateur connecté (manquante dans ton code d'origine)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='orders',
        blank=True,
        null=True,
        help_text="Renseigné si le client a un compte"
    )

    guest = models.OneToOneField(
        GuestInfo,
        on_delete=models.SET_NULL,
        related_name='order',
        blank=True,
        null=True,
        help_text="Renseigné si le client est un invité"
    )
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Code pour la réduction
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    discount_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00, 
        help_text="Montant exact déduit via le coupon"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            # La commande appartient SOIT à un User, SOIT à un Guest (Exclusif)
            models.CheckConstraint(
                condition=(
                    models.Q(user__isnull=False, guest__isnull=True) |
                    models.Q(user__isnull=True,  guest__isnull=False)
                ),
                name='order_user_or_guest_exclusive'
            )
        ]

    def __str__(self):
        owner = self.user.username if self.user else (self.guest.full_name if self.guest else 'Inconnu')
        return f'Commande {str(self.id)[:8]} — {owner} — {self.get_status_display()}'

    @property
    def is_guest_order(self):
        return self.guest is not None

    @property
    def buyer_email(self):
        """Retourne l'email de l'acheteur quel que soit son type."""
        if self.user:
            return self.user.email
        return self.guest.email if self.guest else None

    def update_total(self):
        """Recalcule et sauvegarde le total depuis les lignes (OrderItem)."""
        subtotal = sum(item.get_subtotal() for item in self.order_items.all())
        self.total_amount = max(subtotal - self.discount_amount, 0)
        self.save()

    def can_be_cancelled(self):
        return self.status == self.Status.PENDING

class OrderItem(models.Model):
    """
    Ligne de commande — snapshot complet au moment du checkout.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        name = self.product.name if self.product else "Produit supprimé"
        return f'{self.quantity} x {name} — commande {str(self.order.id)[:8]}'

    def get_subtotal(self):
        return self.unit_price * self.quantity

    def save(self, *args, **kwargs): 
        # On définit le unit_price uniquement s'il n'est pas encore défini
        if self.unit_price is None and self.product:
            self.unit_price = self.product.price # Attention: assure-toi que c'est 'price' et non 'prix' selon ton modèle Product
        elif self.unit_price is None:
            self.unit_price = 0.00
            
        super().save(*args, **kwargs)

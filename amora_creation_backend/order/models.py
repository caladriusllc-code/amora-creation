import uuid
from django.db import models
from django.conf import settings
from product.models import Product
from cart.models import Coupon
from decimal import Decimal

# ==========================================
# 1. NOUVEAUX MODÈLES DE LIVRAISON
# ==========================================

class ShippingZone(models.Model):
    """
    Zone géographique de livraison (ex: Abidjan, Intérieur, International)
    """
    name = models.CharField(max_length=100, verbose_name="Nom de la zone")
    is_active = models.BooleanField(default=True, verbose_name="Zone active")

    class Meta:
        verbose_name = "Zone de livraison"
        verbose_name_plural = "Zones de livraison"

    def __str__(self):
        return self.name

class ShippingRate(models.Model):
    """
    Grille tarifaire croisant la zone et le poids total de la commande
    """
    zone = models.ForeignKey(
        ShippingZone, 
        related_name='rates', 
        on_delete=models.CASCADE, 
        verbose_name="Zone de livraison"
    )
    min_weight = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Poids minimum")
    max_weight = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Poids maximum")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix de la livraison")

    class Meta:
        verbose_name = "Tarif de livraison"
        verbose_name_plural = "Tarifs de livraison"
        ordering = ['zone', 'min_weight']

    def __str__(self):
        return f"{self.zone.name} : {self.min_weight} - {self.max_weight} -> {self.price} FCFA"


# ==========================================
# 2. MODÈLES DE COMMANDE EXISTANTS MIS À JOUR
# ==========================================

class GuestInfo(models.Model):
    """
    Infos de l'invité collectées au checkout.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField()
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)
    
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
    
    # --- AJOUT: Informations de livraison ---
    shipping_zone = models.ForeignKey(
        ShippingZone, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Zone de livraison sélectionnée"
    )
    shipping_fee = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'), 
        verbose_name="Frais de livraison appliqués"
    )

    # --- Tarification de base ---
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # --- Réductions ---
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    discount_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'), 
        help_text="Montant exact déduit via le coupon"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
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
        if self.user:
            return self.user.email
        return self.guest.email if self.guest else None

    def update_total(self):
        """Recalcule et sauvegarde le total depuis les lignes (OrderItem) et ajoute la livraison."""
        subtotal = sum((item.get_subtotal() for item in self.order_items.all()), Decimal('0.00'))
        
        # 1. On applique la réduction au sous-total (ne peut pas être négatif)
        discounted_subtotal = max(subtotal - self.discount_amount, Decimal('0.00'))
        
        # 2. On ajoute les frais de livraison
        self.total_amount = discounted_subtotal + self.shipping_fee
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
        if self.unit_price is None and self.product:
            self.unit_price = self.product.price
        elif self.unit_price is None:
            self.unit_price = 0.00
            
        super().save(*args, **kwargs)
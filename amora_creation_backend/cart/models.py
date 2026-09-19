import uuid
from django.db import models
from django.utils import timezone
from decimal import Decimal
from product.models import Product, Size, Color

class Coupon(models.Model):
    class DiscountType(models.TextChoices):
        PERCENTAGE = 'percentage', 'Pourcentage (%)'
        FIXED = 'fixed', 'Montant fixe (FCFA)'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=50, unique=True, help_text="Ex: BIENTOT_AVOCAT_2026")
    discount_type = models.CharField(max_length=20, choices=DiscountType.choices)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, help_text="Valeur de la réduction")
    
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)
    max_usages = models.PositiveIntegerField(default=100, help_text="Combien de fois ce code peut-il être utilisé en tout ?")
    used_count = models.PositiveIntegerField(default=0)

    def is_valid(self):
        now = timezone.now()
        return self.active and self.valid_from <= now <= self.valid_to and self.used_count < self.max_usages

    def __str__(self):
        return f'{self.code}'


class Cart(models.Model):
    """
        Panier hybride : lié à un user connecté OU à une session invité.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    session_key = models.CharField(
        max_length=40,
        blank=True,
        null=True,
        unique=True,
        help_text="Clé de session Django pour les invités"
    )

    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Panier'

    def __str__(self):
        return f'Panier invité (session {str(self.session_key)[:8]}…)'

    def get_total(self):
        return sum((item.get_subtotal() for item in self.items.all()), Decimal('0.00'))

    # ⚡️ NOUVEAU : Calcule le poids total de tous les articles du panier
    def get_total_weight(self):
        return sum((item.get_weight() for item in self.items.all()), Decimal('0.00'))

    def clear(self):
        self.items.all().delete()

    def get_total_with_discount(self):
        subtotal = self.get_total()
        if self.coupon and self.coupon.is_valid():
            if self.coupon.discount_type == 'percentage':
                discount = (self.coupon.discount_value / Decimal('100')) * subtotal
                return subtotal - discount
            elif self.coupon.discount_type == 'fixed':
                return max(subtotal - self.coupon.discount_value, Decimal('0.00'))
        return subtotal


class CartItem(models.Model):
    """
    Ligne du panier
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='cart_items', 
        null=True, 
        blank=True
    )
    size = models.ForeignKey(
        Size,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cart_items'
    )
    color = models.ForeignKey(
        Color,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cart_items'
    )
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Snapshot du prix au moment de l'ajout"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Article du panier'
        verbose_name_plural = 'Articles du panier'

    def __str__(self):
        return f'{self.quantity}x {self.product.name}'

    def get_subtotal(self):
        return self.unit_price * self.quantity

    # ⚡️ NOUVEAU : Récupère le poids depuis le code du modèle Weight lié au produit
    def get_weight(self):
        if self.product and self.product.weight and self.product.weight.code:
            return self.product.weight.code * self.quantity
        return Decimal('0.00')

    def save(self, *args, **kwargs):
        if not self.unit_price and self.product:
            # 👈 CORRECTION : Remplacement de self.product.prix par self.product.price
            self.unit_price = self.product.price
        super().save(*args, **kwargs)

class GuestInfo(models.Model):
    """
    Infos de l'invité collectées au checkout.
    Lié à la commande (Order) — pas au panier.
    Permet d'envoyer le lien de téléchargement par email.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField()
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
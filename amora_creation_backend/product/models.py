from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """
    Catégories de produits (ex: Robes, T-shirts, Accessoires)
    """
    name = models.CharField(max_length=100, verbose_name="Nom de la catégorie")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name="Description")

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Collection(models.Model):
    """
    Collections thématiques ou saisonnières (ex: Collection Été 2026, Capsule Soirée)
    """
    name = models.CharField(max_length=100, verbose_name="Nom de la collection")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name="Description")
    image = models.ImageField(
        upload_to='collections/',  # Les images seront stockées dans media/collections/
        blank=True,                 # L'image est optionnelle dans les formulaires
        null=True,                  # L'image est optionnelle dans la base de données
        verbose_name="Image de couverture"
    )
    is_active = models.BooleanField(default=True, verbose_name="Collection active")
    is_featured = models.BooleanField(default=False, verbose_name="Collection à la une")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    class Meta:
        verbose_name = "Collection"
        verbose_name_plural = "Collections"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Size(models.Model):
    """
    Tailles des vêtements (ex: XS, S, M, L, XL, 38, 40...)
    """
    name = models.CharField(max_length=20, verbose_name="Nom de la taille")
    code = models.CharField(max_length=10, unique=True, verbose_name="Code unique (ex: S, M, 38)")

    class Meta:
        verbose_name = "Taille"
        verbose_name_plural = "Tailles"
        ordering = ['id']

    def __str__(self):
        return self.name


class Color(models.Model):
    """
    Couleurs disponibles avec code HEX pour affichage des pastilles sur le front-end
    """
    name = models.CharField(max_length=50, verbose_name="Nom de la couleur")
    hex_code = models.CharField(
        max_length=7, 
        blank=True, 
        null=True, 
        verbose_name="Code HEX (ex: #000000)"
    )

    class Meta:
        verbose_name = "Couleur"
        verbose_name_plural = "Couleurs"

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Modèle principal du produit (fiche produit générale)
    """
    name = models.CharField(max_length=200, verbose_name="Nom du produit")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(verbose_name="Description détaillée")

    # Tarification & Marketing
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix de base")
    discount_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        verbose_name="Prix promotionnel (optionnel)"
    )

    # Relations
    category = models.ForeignKey(
        Category, 
        related_name='products', 
        on_delete=models.CASCADE, 
        verbose_name="Catégorie"
    )
    collection = models.ForeignKey(
        Collection, 
        related_name='products', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Collection"
    )

    # Affichage et Visibilité
    is_active = models.BooleanField(default=True, verbose_name="Afficher sur la boutique")
    is_featured = models.BooleanField(default=False, verbose_name="Mettre en avant (Coup de cœur / Nouveauté)")

    # Référencement (SEO)
    meta_title = models.CharField(max_length=150, blank=True, verbose_name="Titre Meta (SEO)")
    meta_description = models.TextField(blank=True, verbose_name="Description Meta (SEO)")

    # Horodatages
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def total_stock(self):
        """Calcule le stock total disponible en additionnant toutes les déclinaisons"""
        return sum(variant.stock for variant in self.variants.all())

    @property
    def is_in_stock(self):
        """Indique si au moins un exemplaire est disponible"""
        return self.total_stock > 0


class ProductVariant(models.Model):
    """
    Déclinaisons exactes d'un produit (Combinaison Produit + Taille + Couleur)
    Permet la gestion précise des stocks et des références SKU.
    """
    product = models.ForeignKey(
        Product, 
        related_name='variants', 
        on_delete=models.CASCADE, 
        verbose_name="Produit"
    )
    size = models.ForeignKey(
        Size, 
        related_name='variants', 
        on_delete=models.CASCADE, 
        verbose_name="Taille"
    )
    color = models.ForeignKey(
        Color, 
        related_name='variants', 
        on_delete=models.CASCADE, 
        verbose_name="Couleur"
    )
    sku = models.CharField(max_length=50, unique=True, verbose_name="Référence SKU (Stock Keeping Unit)")
    stock = models.PositiveIntegerField(default=0, verbose_name="Quantité en stock")
    price_override = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        verbose_name="Prix spécifique à cette variante (si différent)"
    )

    class Meta:
        verbose_name = "Déclinaison de produit"
        verbose_name_plural = "Déclinaisons de produits"
        unique_together = ('product', 'size', 'color')

    def __str__(self):
        return f"{self.product.name} - {self.color.name} / {self.size.name}"

    @property
    def active_price(self):
        """Retourne le prix effectif de cette variante"""
        if self.price_override is not None:
            return self.price_override
        return self.product.discount_price if self.product.discount_price else self.product.price


class ProductImage(models.Model):
    """
    Galerie d'images associées au produit
    """
    product = models.ForeignKey(
        Product, 
        related_name='images', 
        on_delete=models.CASCADE, 
        verbose_name="Produit"
    )
    image = models.ImageField(upload_to='products/%Y/%m/', verbose_name="Image")
    alt_text = models.CharField(max_length=200, blank=True, verbose_name="Texte alternatif (SEO)")
    is_main = models.BooleanField(default=False, verbose_name="Image principale")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")

    class Meta:
        verbose_name = "Image de produit"
        verbose_name_plural = "Images de produits"
        ordering = ['-is_main', 'order', 'id']

    def __str__(self):
        return f"Image pour {self.product.name}"
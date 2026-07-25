from django.contrib import admin
from .models import (
    Category,
    Collection,
    Size,
    Color,
    Product,
    ProductVariant,
    ProductImage
)
# Register your models here.
admin.site.register(Category)
admin.site.register(Collection)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(ProductImage)
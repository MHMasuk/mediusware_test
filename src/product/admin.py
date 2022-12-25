from django.contrib import admin

# need to remove
from .models import Product, ProductImage, ProductVariant, ProductVariantPrice, Variant

# Register your models here.
admin.site.register(Product)
admin.site.register(Variant)
admin.site.register(ProductImage)
admin.site.register(ProductVariant)
admin.site.register(ProductVariantPrice)
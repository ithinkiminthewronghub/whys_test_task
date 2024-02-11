from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import AttributeName, AttributeValue, Attribute, Product, ProductAttributes, Image, ProductImage, Catalog


@admin.register(AttributeName)
class AttributeNameAdmin(admin.ModelAdmin):
    list_display = ['nazev', 'kod', 'zobrazit']
    list_filter = ['zobrazit']


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ['hodnota']


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ['nazev_atributu', 'hodnota_atributu']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['nazev', 'cena', 'mena', 'published_on', 'is_published']
    list_filter = ['is_published']
    search_fields = ['nazev', 'description']


@admin.register(ProductAttributes)
class ProductAttributesAdmin(admin.ModelAdmin):
    list_display = ['attribute', 'product']
    list_filter = ['attribute', 'product']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['nazev', 'obrazek']


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'nazev', 'obrazek_id']


# For some reason, there is an error when trying to get Catalogs in admin panel
# TypeError at /admin/new_eshop/catalog/
# __str__ returned non-string (type NoneType)
# Even though __str__ returns the correct name
@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ['nazev', 'obrazek']


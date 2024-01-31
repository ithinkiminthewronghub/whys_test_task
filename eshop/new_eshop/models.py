"""
Basic models for the database initialization
Names of the models are used from test_data.json
"""

from django.db import models


# Model for AttributeName
class AttributeName(models.Model):
    id = models.IntegerField(primary_key=True)
    nazev = models.CharField(max_length=255, blank=True, null=True)
    kod = models.CharField(max_length=255, blank=True, null=True)
    zobrazit = models.BooleanField(default=False, blank=True, null=True)


# Model for AttributeValue
class AttributeValue(models.Model):
    id = models.IntegerField(primary_key=True)
    hodnota = models.CharField(max_length=255)


# Model for Attribute
class Attribute(models.Model):
    id = models.IntegerField(primary_key=True)
    nazev_atributu_id = models.IntegerField()
    hodnota_atributu_id = models.IntegerField()


# Model for Product
class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    nazev = models.CharField(max_length=255)
    description = models.TextField()
    cena = models.CharField(max_length=10)
    mena = models.CharField(max_length=3)
    published_on = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField()


# Model for ProductAttributes
class ProductAttributes(models.Model):
    id = models.IntegerField(primary_key=True)
    attribute = models.IntegerField()
    product = models.IntegerField()


# Model for Image
class Image(models.Model):
    id = models.IntegerField(primary_key=True)
    nazev = models.CharField(max_length=255, blank=True, null=True)
    obrazek = models.URLField()


# Model for ProductImage
class ProductImage(models.Model):
    id = models.IntegerField(primary_key=True)
    product = models.IntegerField()
    obrazek_id = models.IntegerField()
    nazev = models.CharField(max_length=255)


# Model for Catalog
class Catalog(models.Model):
    id = models.IntegerField(primary_key=True)
    nazev = models.CharField(max_length=255)
    obrazek_id = models.IntegerField()
    products_ids = models.JSONField()
    attributes_ids = models.JSONField()

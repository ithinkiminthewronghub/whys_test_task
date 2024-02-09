"""
Basic models for the database initialization
Names of the models are used from test_data.json
"""

from django.db import models


# Model for AttributeName
class AttributeName(models.Model):

    nazev = models.CharField(max_length=255, blank=True, null=True)
    kod = models.CharField(max_length=255, blank=True, null=True)
    zobrazit = models.BooleanField(default=False)

    def __str__(self):
        return self.nazev


class AttributeValue(models.Model):

    hodnota = models.CharField(max_length=255)

    def __str__(self):
        return self.hodnota


class Attribute(models.Model):

    nazev_atributu = models.ForeignKey(AttributeName, on_delete=models.CASCADE)
    hodnota_atributu = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nazev_atributu}: {self.hodnota_atributu}"


class Product(models.Model):

    nazev = models.CharField(max_length=255)
    description = models.TextField()
    cena = models.DecimalField(max_digits=10, decimal_places=2)
    mena = models.CharField(max_length=3)
    published_on = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField()

    def __str__(self):
        return self.nazev


class ProductAttributes(models.Model):

    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Image(models.Model):

    nazev = models.CharField(max_length=255, blank=True, null=True)
    obrazek = models.URLField()

    def __str__(self):
        return self.nazev


class ProductImage(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    obrazek_id = models.IntegerField()
    nazev = models.CharField(max_length=255)

    def __str__(self):
        return self.nazev


class Catalog(models.Model):

    nazev = models.CharField(max_length=255)
    obrazek = models.ForeignKey(Image, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    attributes = models.ManyToManyField(Attribute)

    def __str__(self):
        return self.nazev

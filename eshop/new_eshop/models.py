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

        return str(self.nazev)


# Model for AttributeValue
class AttributeValue(models.Model):

    hodnota = models.CharField(max_length=255)

    def __str__(self):
        return str(self.hodnota)


# Model for Attribute
class Attribute(models.Model):
    # Using foreign key to exploit the connection between models
    nazev_atributu = models.ForeignKey(AttributeName, on_delete=models.CASCADE, blank=True, null=True)
    hodnota_atributu = models.ForeignKey(AttributeValue, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):

        return str(f"{self.nazev_atributu}: {self.hodnota_atributu}")


# Model for Product
class Product(models.Model):

    nazev = models.CharField(max_length=255)
    description = models.TextField()
    cena = models.DecimalField(max_digits=10, decimal_places=2)
    mena = models.CharField(max_length=3)
    published_on = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField()

    def __str__(self):
        return str(self.nazev)


# Model for ProductAttributes
class ProductAttributes(models.Model):

    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


# Model for Image
class Image(models.Model):

    nazev = models.CharField(max_length=255, blank=True, null=True)
    obrazek = models.URLField()

    def __str__(self):
        if self.obrazek:
            return str(self.nazev)
        elif self.obrazek:
            return str(self.obrazek)


# Model for ProductImage
class ProductImage(models.Model):
    # Id of a product as a foreign key
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    obrazek_id = models.IntegerField()
    nazev = models.CharField(max_length=255)

    def __str__(self):

        return str(self.nazev)


# Model for Catalog
class Catalog(models.Model):

    nazev = models.CharField(max_length=255)
    obrazek_id = models.IntegerField()
    # Implementing many-to-many relations
    # In one catalog many products and attributes can be shown
    products_ids = models.ManyToManyField(Product, related_name='catalogs')
    attributes_ids = models.ManyToManyField(Attribute, related_name='catalogs')

    def __str__(self):
        return str(self.nazev)


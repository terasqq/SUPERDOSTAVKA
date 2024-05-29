from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=64, null=True)
    image = models.ImageField(null=True)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    image = models.ImageField(null=True)
    name = models.CharField(max_length=256, null=True)
    code = models.CharField(max_length=64, default="XXXX-XXX-XXXXX")
    barcode = models.PositiveIntegerField(default=1234567890)
    description = models.TextField(null=True)
    provider = models.CharField(max_length=64, null=True)
    purchase_price = models.PositiveIntegerField(null=True)
    selling_price = models.PositiveIntegerField(null=True)
    amount = models.PositiveIntegerField(default=1)

from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    price = models.CharField(max_length=10)
    quantity = models.CharField(max_length=5)

    def __str__(self):
        return self.name


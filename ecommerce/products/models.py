from django.db import models

from ecommerce.utils.models import BaseModel, SafeModel


class Category(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Product(SafeModel):
    name = models.CharField(max_length=80)
    description = models.TextField(blank=True)
    current_price = models.DecimalField(max_digits=9, decimal_places=2)
    slug = models.SlugField()

    def __str__(self):
        return f'{self.name}, {self.current_price}'

from django.core.validators import MinValueValidator
from django.db import models

from ecommerce.clients.models import Client
from ecommerce.core.models import User
from ecommerce.products.models.composite_models import ProductConfiguration
from ecommerce.utils.models import BaseModel


class Order(BaseModel):
    employee = models.ForeignKey(User, on_delete=models.PROTECT)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    products = models.ManyToManyField(ProductConfiguration,
                                      through='OrderProducts')


class OrderProducts(BaseModel):
    product = models.ForeignKey(ProductConfiguration, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'order'],
                name='product_order_unique_constraint',
            ),
        ]

from django.db import models

from ecommerce.core.models import User
from ecommerce.products.models.composite_models import ProductConfiguration
from ecommerce.utils.models import BaseModel


class Cart(BaseModel):
    products = models.ManyToManyField(ProductConfiguration,
                                      through='CartProducts')
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class CartProducts(BaseModel):
    product = models.ForeignKey(ProductConfiguration, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'cart'],
                name='product_card_unique_constraint',
            ),
        ]

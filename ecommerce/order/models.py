from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import DecimalField, F, Q, Sum

from ecommerce.core.models import User
from ecommerce.products.models.composite_models import ProductConfiguration
from ecommerce.utils.models import BaseModel


class Cart(BaseModel):
    products = models.ManyToManyField(ProductConfiguration,
                                      through='CartProducts')
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    cookie_id = models.UUIDField(null=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=((Q(user__isnull=True) | Q(cookie_id__isnull=True))
                       & ~(Q(user__isnull=True) & Q(cookie_id__isnull=True))),
                name='user_or_cookieid_null'
            )
        ]

    @property
    def cookie_id_str(self) -> str:
        return str(self.cookie_id) if self.cookie_id else ''

    def calculate_total_price(self) -> Decimal:
        return (CartProducts.objects.filter(cart=self).aggregate(
            total_price=Sum(F('product__current_price') * F('quantity'),
                            output_field=DecimalField()))["total_price"])

    def __str__(self) -> str:
        return f'User: {self.user}, cookie: {self.cookie_id}'

    def contains_product(self, product_id: int) -> bool:
        return self.products.filter(product_id=product_id).exists()


class CartProducts(BaseModel):
    product = models.ForeignKey(ProductConfiguration, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1,
                                   validators=[MinValueValidator(1)])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'cart'],
                name='product_card_unique_constraint',
            ),
        ]

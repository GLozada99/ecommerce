from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext as _

from ecommerce.clients.models import Client
from ecommerce.core.models import User
from ecommerce.products.models.composite_models import ProductConfiguration
from ecommerce.utils.models import BaseModel


class Order(BaseModel):
    CASH_DELIVERY = _('Cash on delivery')
    CARD_DELIVERY = _('Card on delivery')
    BANK_TRANSFER_DELIVERY = _('Bank Transfer on delivery')
    PICKUP = _('Payment on pick up')
    PAYMENT_CHOICES = [
        ('Cash', CASH_DELIVERY),
        ('Card', CARD_DELIVERY),
        ('Transfer', BANK_TRANSFER_DELIVERY),
        ('Pickup', PICKUP)
    ]

    payment_type = models.CharField(max_length=8, choices=PAYMENT_CHOICES)
    employee = models.ForeignKey(User, on_delete=models.PROTECT)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    products = models.ManyToManyField(ProductConfiguration,
                                      through='OrderProducts')
    completed = models.BooleanField(default=False)

    @classmethod
    @property
    def payment_choices(cls) -> list[str]:
        return [choice[1] for choice in cls.PAYMENT_CHOICES]

    def needs_delivery(self) -> bool:
        return self.payment_type != self.PICKUP


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

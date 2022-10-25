from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext as _
from djchoices import ChoiceItem, DjangoChoices

from ecommerce.clients.models import Client
from ecommerce.core.models import User
from ecommerce.products.models.composite_models import ProductConfiguration
from ecommerce.utils.models import BaseModel


class Order(BaseModel):
    class PaymentChoices(DjangoChoices):
        CASH_DELIVERY = ChoiceItem('Cash', _('Cash on delivery'))
        CARD_DELIVERY = ChoiceItem('Card', _('Card on delivery'))
        BANK_TRANSFER_DELIVERY = ChoiceItem(
            'Transfer', _('Bank Transfer on delivery')
        )
        PICKUP = ChoiceItem('Pickup', _('Payment on pick up'))

    payment_type = models.CharField(max_length=8,
                                    choices=PaymentChoices.choices)
    employee = models.ForeignKey(User, on_delete=models.PROTECT,
                                 related_name='orders_to_manage')
    client = models.ForeignKey(Client, on_delete=models.PROTECT,
                               related_name='orders')
    products = models.ManyToManyField(ProductConfiguration,
                                      through='OrderProducts')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    completed = models.BooleanField(default=False)
    info = models.TextField(null=True, blank=True)

    @classmethod
    @property
    def payment_choices(cls) -> list[dict[str, str]]:
        return [{'value': value, 'label': label} for value, label
                in cls.PaymentChoices.values.items()]

    def needs_delivery(self) -> bool:
        return self.payment_type != self.PaymentChoices.PICKUP


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

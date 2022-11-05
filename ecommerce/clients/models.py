from django.db import models
from django.db.models import Model
from django.utils.translation import gettext_lazy as _

from ecommerce.core.models import User
from ecommerce.utils.models import SafeModel


class Client(SafeModel):
    user = models.OneToOneField(User, on_delete=models.PROTECT,
                                related_name='client_profile')

    class Meta:
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")

    def __str__(self) -> str:
        return f'{self.user}'


class Address(Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE,
                               related_name='addresses')
    state = models.CharField(_("state"), max_length=40)
    city = models.CharField(_("city"), max_length=40)
    first_line = models.CharField(
        _("first line"),
        max_length=100,
        help_text='Sector, Street'
    )
    second_line = models.CharField(
        _("second line"),
        max_length=100,
        help_text='Building, Apartment, Floor, House No.'
    )

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    def __str__(self) -> str:
        return (f'{self.state}, {self.city}:\n'
                f'{self.first_line};\n'
                f'{self.second_line}')

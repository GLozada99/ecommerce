from django.db import models
from django.db.models import Model

from ecommerce.core.models import User
from ecommerce.utils.models import SafeModel


class Client(SafeModel):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    phone = models.CharField(max_length=30)
    authentication_provider = models.TextField()

    def __str__(self) -> str:
        return f'{self.user}\n{self.authentication_provider}'


class Address(Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    state = models.CharField(max_length=40)
    city = models.CharField(max_length=40)
    first_line = models.CharField(
        max_length=100, help_text='Sector, Street')
    second_line = models.CharField(
        max_length=100, help_text='Building, Apartment, Floor, House No.')

    class Meta:
        verbose_name_plural = 'Addresses'

    def __str__(self) -> str:
        return (f'{self.state}, {self.city}\n'
                f'{self.first_line}\n'
                f'{self.second_line}')

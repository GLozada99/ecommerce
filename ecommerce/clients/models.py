from django.db import models
from django.utils.translation import gettext_lazy as _

from ecommerce.utils.models import SafeModel


class Client(SafeModel):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(_('email address'), blank=True, unique=True)
    authentication_provider = models.TextField()

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}, {self.email}'

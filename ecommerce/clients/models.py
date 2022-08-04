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

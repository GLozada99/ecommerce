from django.contrib.auth.models import AbstractUser

from ecommerce.utils.models import BaseModel


class User(AbstractUser, BaseModel):

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}, {self.email}'

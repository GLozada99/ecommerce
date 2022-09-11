from django.contrib.auth.models import AbstractUser
from django.db import models
from thumbnails.fields import ImageField

from ecommerce.utils.models import BaseModel


class User(AbstractUser, BaseModel):

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}, {self.email}'


class SlideImage(BaseModel):
    text = models.CharField(max_length=60)
    image = ImageField(upload_to='slide/', pregenerated_sizes=['slide'])

    def frontpage_picture_url(self) -> str:
        return self.image.thumbnails.slide.url

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from thumbnails.fields import ImageField

from ecommerce.utils.models import BaseModel


class User(AbstractUser, BaseModel):
    phone = models.CharField(_("phone"), max_length=30, null=True,
                             blank=True)
    email = models.EmailField(_("email address"), blank=True)

    def __str__(self) -> str:
        return f'{self.username}, {self.email}'

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class SlideImage(BaseModel):
    text = models.CharField(_("text"), max_length=60)
    image = ImageField(_("image"), upload_to='slide/',
                       pregenerated_sizes=['slide'])
    show = models.BooleanField(_("show"), default=False)
    order = models.PositiveIntegerField(_("order"), unique=True)

    def frontpage_picture_url(self) -> str:
        return self.image.thumbnails.slide.url

    class Meta:
        verbose_name = _("Slide Image")
        verbose_name_plural = _("Slide Images")

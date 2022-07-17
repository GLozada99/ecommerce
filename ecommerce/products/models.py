from django.db import models

from ecommerce.utils.models import BaseModel


class Type(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

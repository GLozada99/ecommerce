from django.db import models
from thumbnails.fields import ImageField

from ecommerce.utils.models import BaseModel, SafeModel


class Category(BaseModel):
    name = models.CharField(max_length=255)
    icon = ImageField(upload_to='category/',
                      pregenerated_sizes=['category_frontpage']
                      )
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'

    def __str__(self) -> str:
        return self.name

    def frontpage_picture_url(self) -> str:
        return self.icon.thumbnails.category_frontpage.url


class Product(SafeModel):
    name = models.TextField()
    general_description = models.TextField(blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True
    )
    slug = models.SlugField()

    def __str__(self) -> str:
        return f'{self.name}, {self.category}'

    @property
    def first_config(self) -> BaseModel:
        return self.configurations.order_by('pk').first()

    @property
    def general_description_paragraphs(self) -> list[str]:
        return self.general_description.split('\r\n\r\n')

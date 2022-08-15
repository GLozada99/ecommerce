from django.core.validators import FileExtensionValidator
from django.db import models

from ecommerce.utils.models import BaseModel, SafeModel


class Category(BaseModel):
    name = models.CharField(max_length=255)
    icon = models.FileField(upload_to='category/',
                            validators=[
                               FileExtensionValidator(['svg'])
                            ])
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'

    def __str__(self) -> str:
        return self.name


class Product(SafeModel):
    name = models.CharField(max_length=80)
    general_description = models.TextField(blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True
    )
    slug = models.SlugField()

    def __str__(self) -> str:
        return f'{self.name}, {self.category}'

    @property
    def general_description_paragraphs(self) -> list[str]:
        return self.general_description.split('\r\n\r\n')

    @property
    def principal_image_list_url(self) -> str:
        return self.types.first().pictures.first().list_url

    @property
    def principal_image_detail_url(self) -> str:
        return self.types.first().pictures.first().list_url

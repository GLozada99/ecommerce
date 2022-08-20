from decimal import Decimal

from django.db import models
from thumbnails.fields import ImageField

from ecommerce import settings
from ecommerce.utils.models import BaseModel, SafeModel


class Category(BaseModel):
    name = models.CharField(max_length=255)
    icon = ImageField(upload_to='category/')
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'

    def __str__(self) -> str:
        return self.name

    def picture_url(self) -> str:
        return self.icon.thumbnails.large.url


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
    def current_price(self) -> Decimal:
        return self.configurations.first().current_price

    @property
    def general_description_paragraphs(self) -> list[str]:
        return self.general_description.split('\r\n\r\n')

    @property
    def principal_image_list_url(self) -> str:
        return self.configurations.first().picture_list_url

    def n_small_thumbnails_data(self) -> list[dict[str, str]]:
        images_product = self.pictures.all()[
                         :settings.env_settings.SMALL_THUMBNAIL_NUMBER]
        urls = [
            {
                'url': str(image_data.image.thumbnails.small.url),
                'id': str(image_data.id),
            }
            for image_data in images_product
        ]
        return urls

    def configuration_data(self) -> list[dict[str, str | int | Decimal]]:
        return [
            {
                'id': data.id,
                'name': data.name,
                'current_price': data.current_price,
                'url': data.picture.thumbnails.small.url,
            } for data in self.configurations.all()
        ]

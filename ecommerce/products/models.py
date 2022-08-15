from django.core.validators import FileExtensionValidator
from django.db import models
from thumbnails.fields import ImageField

from ecommerce import settings
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
    description = models.TextField(blank=True)
    long_description = models.TextField(blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True
    )
    current_price = models.DecimalField(max_digits=9, decimal_places=2)
    slug = models.SlugField()

    def __str__(self) -> str:
        return f'{self.name}, {self.current_price}'

    @property
    def principal_image_list_url(self) -> str:
        return self.pictures.first().list_url

    @property
    def principal_image_detail_url(self) -> str:
        return self.pictures.first().detail_url

    @property
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
        print(urls)
        return urls


class ImageProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT,
                                related_name='pictures')
    image = ImageField(upload_to='products/')

    @property
    def detail_url(self) -> str:
        return self.image.thumbnails.large.url

    @property
    def list_url(self) -> str:
        return self.image.thumbnails.medium.url

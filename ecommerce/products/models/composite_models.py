from django.db import models
from thumbnails.fields import ImageField

from ecommerce import settings
from ecommerce.products.models.models import Product


class TypeProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT,
                                related_name='types')
    name = models.CharField(max_length=80)
    description = models.TextField(blank=True)
    current_price = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self) -> str:
        return f'{self.product}\n{self.name}'

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
        return urls


class ImageProduct(models.Model):
    product = models.ForeignKey(TypeProduct, on_delete=models.PROTECT,
                                related_name='pictures')
    image = ImageField(upload_to='products/')

    @property
    def detail_url(self) -> str:
        return self.image.thumbnails.large.url

    @property
    def list_url(self) -> str:
        return self.image.thumbnails.medium.url


class ExtraDataProduct(models.Model):
    product = models.ForeignKey(TypeProduct, on_delete=models.CASCADE,
                                related_name='extra_data')
    name = models.CharField(max_length=30)
    value = models.CharField(max_length=50)

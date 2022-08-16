from django.db import models
from thumbnails.fields import ImageField

from ecommerce.products.models.models import Product


class ProductConfiguration(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT,
                                related_name='configurations')
    name = models.TextField()
    picture = ImageField(upload_to='products/configuration/')
    description = models.TextField(blank=True)
    current_price = models.DecimalField(max_digits=9, decimal_places=2)
    slug = models.SlugField()

    def __str__(self) -> str:
        return f'{self.product}\n{self.name}'

    @property
    def picture_detail_url(self) -> str:
        return self.picture.thumbnails.large.url

    @property
    def picture_list_url(self) -> str:
        return self.picture.thumbnails.medium.url


class ProductPicture(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT,
                                related_name='pictures')
    picture = ImageField(upload_to='products/general/')

    @property
    def detail_url(self) -> str:
        return self.picture.thumbnails.large.url

    @property
    def list_url(self) -> str:
        return self.picture.thumbnails.medium.url


class ProductExtraData(models.Model):
    product = models.ForeignKey(ProductConfiguration, on_delete=models.CASCADE,
                                related_name='extra_data')
    name = models.CharField(max_length=30)
    value = models.CharField(max_length=50)

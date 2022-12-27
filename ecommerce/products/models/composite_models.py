from django.db import models
from django.utils.translation import gettext_lazy as _
from thumbnails.fields import ImageField

from ecommerce.products.models.models import Product
from ecommerce.utils.models import BaseModel


class ProductConfiguration(BaseModel):
    store_id = models.CharField(_('store id'), max_length=255, blank=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT,
                                related_name='configurations')
    name = models.TextField(_('name'))
    picture = ImageField(_('picture'),
                         upload_to='products/configurations/',
                         pregenerated_sizes=['small', 'medium', 'product_list']
                         )
    description = models.TextField(_('description'), blank=True)
    current_price = models.DecimalField(_('current price'),
                                        max_digits=9, decimal_places=2)
    slug = models.SlugField()

    class Meta:
        verbose_name = _('Product Configuration')
        verbose_name_plural = _('Product Configurations')

    def __str__(self) -> str:
        return f'{self.product}\n{self.name}'

    @property
    def general_name(self) -> str:
        return self.product.name

    @property
    def detail_thumbnail_url(self) -> str:
        return self.picture.thumbnails.small.url

    @property
    def cart_success_url(self) -> str:
        return self.picture.thumbnails.medium.url

    @property
    def list_url(self) -> str:
        return self.picture.thumbnails.product_list.url


class ProductPicture(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.PROTECT,
                                related_name='pictures')
    picture = ImageField(_('picture'),
                         upload_to='products/general/',
                         pregenerated_sizes=[
                             'product_list', 'product_detail',
                             'product_detail_related',
                         ])

    class Meta:
        verbose_name = _('Product Picture')
        verbose_name_plural = _('Product Pictures')

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

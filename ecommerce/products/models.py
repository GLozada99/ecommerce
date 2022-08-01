from django.core.validators import FileExtensionValidator
from django.db import models
from thumbnails.fields import ImageField

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
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True
    )
    current_price = models.DecimalField(max_digits=9, decimal_places=2)
    slug = models.SlugField()

    def __str__(self) -> str:
        return f'{self.name}, {self.current_price}'

    @property
    def principal_image_url(self) -> str:
        first_image = self.pictures.first().image.thumbnails.medium
        return str(first_image.url)


class ImageProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT,
                                related_name='pictures')
    image = ImageField(upload_to='products/')

from django.contrib import admin

from ecommerce.products.models.composite_models import (ProductConfiguration,
                                                        ProductExtraData,
                                                        ProductImage, )


class ImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0


class ExtraDataInline(admin.TabularInline):
    model = ProductExtraData
    extra = 0


class ConfigurationInline(admin.StackedInline):
    model = ProductConfiguration
    extra = 0

from django.contrib import admin

from ecommerce.products.models.composite_models import (ProductConfiguration,
                                                        ProductExtraData,
                                                        ProductPicture, )


class ImageInline(admin.TabularInline):
    model = ProductPicture
    extra = 1
    min = 1


class ExtraDataInline(admin.TabularInline):
    model = ProductExtraData
    extra = 0


class ConfigurationInline(admin.StackedInline):
    model = ProductConfiguration
    extra = 1
    min = 1

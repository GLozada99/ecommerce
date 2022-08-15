from django.contrib import admin

from ecommerce.products.models.composite_models import (ExtraDataProduct,
                                                        ImageProduct,
                                                        TypeProduct, )


class ImageProductInline(admin.TabularInline):
    model = ImageProduct
    extra = 0


class ExtraDataInline(admin.TabularInline):
    model = ExtraDataProduct
    extra = 0


class TypeProductInline(admin.StackedInline):
    model = TypeProduct
    extra = 0

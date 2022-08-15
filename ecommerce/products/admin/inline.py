from django.contrib import admin

from ecommerce.products.models import (ExtraDataProduct,
                                       ImageProduct, )


class ImageProductInline(admin.TabularInline):
    model = ImageProduct


class ExtraDataInline(admin.TabularInline):
    model = ExtraDataProduct

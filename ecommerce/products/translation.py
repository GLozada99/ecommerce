from modeltranslation.translator import TranslationOptions, register

from ecommerce.products.models.composite_models import ProductConfiguration
from ecommerce.products.models.models import Category, Product


@register(Category)
class CategoryTranslation(TranslationOptions):
    fields = ('name',)


@register(Product)
class ProductTranslation(TranslationOptions):
    fields = ('name', 'general_description')


@register(ProductConfiguration)
class TypeProductTranslation(TranslationOptions):
    fields = ('name', 'description')

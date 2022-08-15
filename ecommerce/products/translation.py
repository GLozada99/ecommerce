from modeltranslation.translator import TranslationOptions, register

from ecommerce.products.models.composite_models import TypeProduct
from ecommerce.products.models.models import Category, Product


@register(Category)
class CategoryTranslation(TranslationOptions):
    fields = ('name',)


@register(Product)
class ProductTranslation(TranslationOptions):
    fields = ('name', 'general_description')


@register(TypeProduct)
class TypeProductTranslation(TranslationOptions):
    fields = ('name', 'description')

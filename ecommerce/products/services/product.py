from typing import Mapping

from django.db.models import OuterRef, QuerySet, Subquery

from ecommerce.products.models.composite_models import ProductConfiguration
from ecommerce.products.models.models import Product
from ecommerce.products.services.category import CategoryService


class ProductListService:
    @classmethod
    def get_products(cls, queryset: QuerySet, order_by: str) -> QuerySet:
        configurations_subquery = cls._get_configurations_subquery()
        return queryset.annotate(
            current_price=Subquery(
                configurations_subquery.values('current_price')[:1],
            ),
            current_config_id=Subquery(
                configurations_subquery.values('pk')[:1],
            ),
        ).order_by(order_by if order_by else 'pk')

    @staticmethod
    def _get_configurations_subquery() -> QuerySet:
        return ProductConfiguration.objects.filter(
            product=OuterRef('pk')).order_by('pk')

    @classmethod
    def get_context(cls, raw_data: Mapping) -> dict:
        categories = CategoryService.get_categories()
        current_category = raw_data.get('category', '')
        current_category_dict = cls.get_current_category(current_category,
                                                         categories)
        return {
            'categories': categories,
            'current_category': current_category_dict,
            'current_order_by': raw_data.get('order_by', ''),
        }

    @classmethod
    def get_current_category(
            cls,
            current_category_slug: str,
            categories: QuerySet | None = None) -> Mapping:

        if not categories:
            categories = CategoryService.get_categories()

        return (categories.filter(slug=current_category_slug).
                values('name', 'slug').first()
                if current_category_slug else {'name': '', 'slug': ''})

    @classmethod
    def get_random_products(cls, product_number: int) -> QuerySet:
        return (cls.get_products(
            Product.objects.all(), '').order_by('?')[:product_number]
        )

    @classmethod
    def get_configuration(cls, configuration_id: int) -> Product:
        return (ProductConfiguration.objects.
                filter(pk=configuration_id).first())


class ProductDetailService:
    def __init__(self, product: Product):
        self.product = product

    def get_product_configuration(self, id: int) -> ProductConfiguration:
        try:
            configuration = self.product.configurations.get(id=id)
        except ProductConfiguration.DoesNotExist:
            configuration = self.product.configurations.first()
        return configuration

    def get_product_thumbnails(self, number: int = 5) -> list[dict[str, str]]:

        configurations_thumbnail_data = [
            {
                'url': str(configurations.picture.thumbnails.small.url),
                'id': str(configurations.id),
                'type': 'configurations'
            }
            for configurations in self.product.configurations.all()
        ]

        general_thumbnail_data = [
            {
                'url': str(pictures.picture.thumbnails.small.url),
                'id': str(pictures.id),
                'type': 'pictures'
            }
            for pictures in self.product.pictures.all()[:number]
        ]

        return configurations_thumbnail_data + general_thumbnail_data

    def get_product_picture_url(self, type_: str, id: int) -> str:
        return getattr(self.product, type_).get(
            id=id).picture.thumbnails.product_detail.url

    def get_config_extra_data(
            self, configuration: ProductConfiguration
    ) -> dict:
        return configuration.extra_data.all()

    def get_configurations_data(self) -> list[dict[str, str | int]]:
        return [
            {
                'id': data.id,
                'name': data.name,
                'current_price': str(data.current_price),
                'url': data.picture.thumbnails.small.url,
            } for data in self.product.configurations.all()
        ]

    def get_related_products(self, product_limit: int) -> list:
        products = ProductListService.get_products(
            self.product.category.product_set.all().exclude(
                id=self.product.id),
            '',
        )
        product_count = products.count()
        selected_products = products[:max(product_limit, product_count)]
        return [
            {'product': product,
             'picture_url': (product.first_config.picture.
                             thumbnails.product_detail_related.url)
             } for product in selected_products
        ]

    def get_context(self, config_id: int, product_limit: int) -> dict:
        current_configuration = self.get_product_configuration(config_id)
        return {
            'thumbnails': self.get_product_thumbnails(),
            'current_configuration': current_configuration,
            'configurations': self.get_configurations_data(),
            'current_detail_picture': (current_configuration.picture.
                                       thumbnails.product_detail.url),
            'current_extra_data': self.get_config_extra_data(
                current_configuration),
            'related_products': self.get_related_products(product_limit)
        }

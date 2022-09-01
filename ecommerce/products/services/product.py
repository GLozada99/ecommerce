from django.db.models import OuterRef, QuerySet, Subquery

from ecommerce.products.models.composite_models import ProductConfiguration
from ecommerce.products.models.models import Product


class ProductListService:
    @classmethod
    def get_products(cls, queryset: QuerySet, order_by: str) -> QuerySet:
        configurations_subquery = cls._get_configurations_subquery()
        return queryset.annotate(
            current_price=Subquery(
                configurations_subquery.values('current_price')[:1]
            ),
        ).order_by(order_by if order_by else 'pk')

    @staticmethod
    def _get_configurations_subquery() -> QuerySet:
        return ProductConfiguration.objects.filter(
            product=OuterRef('pk')).order_by('pk')


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

        return general_thumbnail_data + configurations_thumbnail_data

    def get_product_picture_url(self, type_: str, id: int) -> str:
        return getattr(self.product, type_).get(
            id=id).picture.thumbnails.large.url

    def get_configurations_data(self) -> list[dict[str, str | int]]:
        return [
            {
                'id': data.id,
                'name': data.name,
                'current_price': str(data.current_price),
                'url': data.picture.thumbnails.small.url,
            } for data in self.product.configurations.all()
        ]

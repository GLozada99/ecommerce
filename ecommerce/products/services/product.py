from django.db.models import OuterRef, QuerySet, Subquery

from ecommerce.products.models.composite_models import ProductConfiguration


class ProductService:

    @classmethod
    def get_products(cls, queryset: QuerySet, order_by: str) -> QuerySet:
        configurations = cls._get_configurations()
        return queryset.annotate(
            current_price=Subquery(
                configurations.values('current_price')[:1]
            )
        ).order_by(order_by if order_by else 'name')

    @classmethod
    def _get_configurations(cls) -> QuerySet:
        return ProductConfiguration.objects.filter(
            product=OuterRef('pk')).order_by('pk')

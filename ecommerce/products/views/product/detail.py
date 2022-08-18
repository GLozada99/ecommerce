from typing import Mapping

from django.views.generic import DetailView

from ecommerce.products.models.models import Product
from ecommerce.products.services.product import ProductService


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    context_object_name = 'product'
    template_name = 'detail.html'

    def get_context_data(self, **kwargs: dict) -> Mapping:
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        extra = ProductService.get_detail_extra_context(
            self.get_object(),
            self.request.GET,
        )
        return context | extra

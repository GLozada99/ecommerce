from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView

from ecommerce.products.models.models import Product
from ecommerce.products.services.product import ProductDetailService


class ProductDetailView(DetailView):
    queryset = Product.objects.prefetch_related(
        'category', 'configurations').all()
    context_object_name = 'product'

    def get_context_data(self, **kwargs: Any) -> Mapping:
        context = super().get_context_data(**kwargs)
        service = ProductDetailService(self.get_object())
        context |= service.get_context(
            int(self.request.GET.get('config_id', 0)),
            product_limit=4,
        )
        return context


def selected_picture_view(request: HttpRequest, slug: str, type: str,
                          id: int) -> HttpResponse:
    service = ProductDetailService(Product.objects.get(slug=slug))
    context = {
        'current_detail_picture': service.get_product_picture_url(type, id),
    }
    return render(request, 'detail/product_detail_picture.html', context)

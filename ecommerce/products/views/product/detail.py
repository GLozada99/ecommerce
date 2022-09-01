from typing import Mapping

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView

from ecommerce.products.models.models import Product
from ecommerce.products.services.product import ProductDetailService


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    context_object_name = 'product'
    template_name = 'detail.html'

    def get_context_data(self, **kwargs: dict) -> Mapping:
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['current_detail_picture'] = (self.get_object().
                                             pictures.first().detail_url)
        return context


def selected_picture_view(request: HttpRequest, slug: str, type_: str,
                          id: int) -> HttpResponse:
    service = ProductDetailService(Product.objects.get(slug=slug))

    context = {
        'current_detail_picture': service.get_product_picture_url(type_, id)
    }
    return render(request, 'detail/product_zoom.html', context)

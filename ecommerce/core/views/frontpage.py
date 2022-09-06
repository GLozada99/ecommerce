from typing import Mapping

from django.views.generic import TemplateView

from ecommerce.products.services.category import CategoryService
from ecommerce.products.services.product import ProductListService


class FrontPageView(TemplateView):
    template_name = 'frontpage.html'

    def get_context_data(self, **kwargs: dict) -> Mapping:
        context = super(FrontPageView, self).get_context_data(**kwargs)
        product_limit = 8
        context['categories'] = CategoryService.get_categories()
        context['products'] = (ProductListService.
                               get_random_products(product_limit))
        context['slides'] = [
            {'url': 'front1.png', 'text': 'Shopping Day'},
            {'url': 'front2.png', 'text': 'Summer Sale'},
            {'url': 'front3.png', 'text': 'Back to School'},
        ]
        return context

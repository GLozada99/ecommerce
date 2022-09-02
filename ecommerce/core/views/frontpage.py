from typing import Mapping

from django.views.generic import TemplateView

from ecommerce.products.services.category import CategoryService


class FrontPageView(TemplateView):
    template_name = 'frontpage.html'

    def get_context_data(self, **kwargs: dict) -> Mapping:
        context = super(FrontPageView, self).get_context_data(**kwargs)
        context['categories'] = CategoryService.get_categories()
        return context

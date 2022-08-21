from typing import Mapping

from django.views.generic import TemplateView

from ecommerce.products.models.models import Category


class FrontPageView(TemplateView):
    template_name = 'frontpage.html'

    def get_context_data(self, **kwargs: dict) -> Mapping:
        context = super(FrontPageView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

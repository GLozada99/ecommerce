from typing import Mapping

from django.views.generic import TemplateView

from ecommerce.core.services.frontpage import FrontPageService


class FrontPageView(TemplateView):
    template_name = 'frontpage.html'

    def get_context_data(self, **kwargs: dict) -> Mapping:
        context = super().get_context_data(**kwargs)
        context |= FrontPageService.get_context(slide_limit=3,
                                                product_limit=8)
        return context

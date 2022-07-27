from django.views.generic import TemplateView  # type: ignore

from ecommerce.products.services.category import CategoryService


class FrontPageView(TemplateView):
    template_name = 'core/frontpage.html'

    def get_context_data(self, **kwargs):
        context = super(FrontPageView, self).get_context_data(**kwargs)
        context['categories'] = CategoryService.get_categories()
        return context

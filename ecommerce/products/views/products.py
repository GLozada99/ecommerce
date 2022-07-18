from django.views.generic import TemplateView


class ProductListView(TemplateView):
    template_name = 'products/list.html'

    def get(self, request, **kwargs):
        return self.render_to_response({})

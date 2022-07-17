from django.views.generic import TemplateView


class FrontPageView(TemplateView):
    template_name = 'core/frontpage.html'

    def get(self, request, **kwargs):
        return self.render_to_response({})

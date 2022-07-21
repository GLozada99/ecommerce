from django.views.generic import TemplateView

from ecommerce.products.models import Category
from ecommerce.products.serializers.category import CategorySerializer


class FrontPageView(TemplateView):
    template_name = 'core/frontpage.html'

    def get(self, request, **kwargs):
        categories = CategorySerializer(Category.objects.all(), many=True).data
        return self.render_to_response({'categories': categories})

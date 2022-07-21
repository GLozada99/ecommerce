from django.views.generic import TemplateView

from ecommerce.products.models import Product
from ecommerce.products.serializers.product import ProductSerializer


class ProductListView(TemplateView):
    template_name = 'products/list.html'

    def get(self, request, **kwargs):
        products = ProductSerializer(Product.objects.all(), many=True).data
        return self.render_to_response({'products': products})

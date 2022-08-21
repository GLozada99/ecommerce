from django.views.generic import DetailView

from ecommerce.products.models.models import Product


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    context_object_name = 'product'
    template_name = 'detail.html'

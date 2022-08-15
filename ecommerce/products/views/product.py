from typing import Mapping, Sequence

from django.views.generic import DetailView, ListView

from ecommerce.products.models import Product
from ecommerce.products.services.category import CategoryService
from ecommerce.products.services.product import ProductService


class ProductListView(ListView):
    queryset = Product.objects.all()
    context_object_name = 'products'
    paginate_by = 6
    template_name = 'list.html'

    def get_queryset(self) -> Sequence[Product]:
        return ProductService.get_products(
            self.request.GET.get('category'),
            self.request.GET.get('order_by', ''),
        )

    def get_context_data(self, **kwargs: dict) -> Mapping:
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['current_category'] = CategoryService.get_current_category(
            self.request.GET.get('category'),
        )
        context['categories'] = CategoryService.get_categories()
        context['order_by_options'] = ProductService.get_order_by_options()
        context['current_order_by'] = self.request.GET.get('order_by', '')
        return context


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    context_object_name = 'product'
    template_name = 'detail.html'

    def get_context_data(self, **kwargs: dict) -> Mapping:
        context = super(ProductDetailView, self).get_context_data(**kwargs)

        if detail_image_id := int(self.request.GET.get('image_id', 0)):
            context['detail_image_url'] = (ProductService.
                                           get_detail_picture(detail_image_id))
        else:
            context['detail_image_url'] = (self.get_object().
                                           principal_image_detail_url)

        return context

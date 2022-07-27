from django.views.generic import TemplateView  # type: ignore

from ecommerce.products.services.category import CategoryService
from ecommerce.products.services.product import ProductService


class ProductListView(TemplateView):
    template_name = 'products/list.html'

    def get(self, request, **kwargs):
        current_order_by = request.GET.get('order_by', '')
        order_by_options = ProductService.get_order_by_options()

        current_category = CategoryService.get_current_category(
            request.GET.get('category')
        )
        products = ProductService.get_products(
            request.GET.get('category'), current_order_by
        )
        categories = CategoryService.get_short_categories()

        return self.render_to_response(
            {
                'products': products,
                'categories': categories,
                'current_category': current_category,
                'current_order_by': current_order_by,
                'order_by_options': order_by_options,
            }
        )

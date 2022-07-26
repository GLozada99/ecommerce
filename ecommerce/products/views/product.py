from django.views.generic import TemplateView  # type: ignore

from ecommerce.products.services.category import CategoryService
from ecommerce.products.services.product import ProductService


class ProductListView(TemplateView):
    template_name = 'products/list.html'

    def get(self, request, **kwargs):
        current_category = CategoryService.get_current_category(
            request.GET.get('category')
        )
        products = ProductService.get_products(request.GET.get('category'))
        categories = CategoryService.get_short_categories()

        return self.render_to_response(
            {
                'products': products,
                'categories': categories,
                'current_category': current_category
            }
        )

from django.views.generic import TemplateView

from ecommerce.products.models import Product


class ProductListView(TemplateView):
    template_name = 'products/list.html'

    def get(self, request, **kwargs):
        products = get_product_list_data(Product.objects.all())

        return self.render_to_response({'products': products})


def get_product_list_data(products: list) -> list[dict]:
    return [
        {
            'name': product.name,
            'current_price': product.current_price,
            'picture': product.pictures.first(
            ).image.thumbnails.medium.url,
        }
        for product in products
    ]

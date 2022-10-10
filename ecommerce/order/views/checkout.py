from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.views.generic import ListView

from ecommerce.order.mixins import CartViewActionMixin
from ecommerce.order.services.cart import CartInfoService, CartService


class CheckoutView(LoginRequiredMixin, ListView, CartViewActionMixin):
    template_name = 'checkout.html'
    context_object_name = 'products_data'
    paginate_by = 6

    def get_queryset(self) -> QuerySet:
        service = CartService(self.request.user,
                              self.request.COOKIES.get('cookie_id', ''))
        return CartInfoService.get_product_data(service.cart)

    # def get_context_data(self, *, object_list=None, **kwargs: Any) ->
    # Mapping:
    #     states = CheckoutService.get_states()
    #     cities = CheckoutService.get_cities(
    #         int(self.request.GET.get('state_id', 1)))
    #     return {
    #         'states': states,
    #         'cities': cities,
    #     }

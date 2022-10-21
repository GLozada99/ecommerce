from django.db.transaction import atomic
from django.http import HttpRequest

from ecommerce.clients.models import Client
from ecommerce.core.models import User
from ecommerce.core.services.mail import MailService
from ecommerce.order.models.order import Order, OrderProducts
from ecommerce.order.services.cart import CartInfoService, CartService


class CheckoutService:

    def __init__(self, request: HttpRequest):
        self.request = request

    def get_client_profile(self) -> Client:
        try:
            return self.request.user.client_profile
        except AttributeError:
            return Client.objects.create(user=self.request.user)

    def get_checkout_info_context(self) -> dict:
        user: User = self.request.user
        return {
            'addresses': self.get_client_profile().addresses.all(),
            'phone': user.phone or '',
            'email': user.email or '',
            'payment_types': Order.payment_choices,
            'delivery': 1,
        }

    @atomic  # type: ignore
    def create_order(self) -> None:
        # TODO: Breakdown method and use messages if cart is empty (create
        #  custom exeption)
        #  Implement mail templates on the simplest way
        cart_service = CartService(self.request.user, '')
        post_data = self.request.POST.dict()
        client = self.get_client_profile()
        client.user.phone = post_data.get('cellphone')
        client.user.email = post_data.get('email')
        data = {
            'employee': self._get_employee(),
            'client': client,
            'payment_type': (Order.PaymentChoices.PICKUP
                             if not post_data.get('delivery') else
                             Order.PaymentChoices.get_choice(
                                 post_data.get('payment'))).value,
            'info': post_data.get('info')
        }

        order = Order.objects.create(**data)
        order_products = [OrderProducts(
            product=cart_product.product,
            order=order,
            quantity=cart_product.quantity,
            price=cart_product.price
        ) for cart_product in CartInfoService.get_product_data(
            cart_service.cart)]
        OrderProducts.objects.bulk_create(order_products)
        cart_service.delete_all()
        MailService.send_order_mails(order)

    @staticmethod
    def _get_employee() -> User:
        return User.objects.filter(is_staff=True, is_active=True).first()

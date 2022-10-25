from django.db.models import QuerySet
from django.db.transaction import atomic

from ecommerce.clients.models import Client
from ecommerce.core.models import User
from ecommerce.core.services.mail import MailService
from ecommerce.order.models.cart import Cart, CartProducts
from ecommerce.order.models.order import Order, OrderProducts
from ecommerce.order.services.cart import CartInfoService, CartService


class CheckoutService:

    def __init__(self, user: User, post_data: dict):
        self.user = user
        self.post_data = post_data
        self.__client: None | Client = None

    @property
    def client(self) -> Client:
        if self.__client:
            return self.__client

        try:
            client = self.user.client_profile
        except AttributeError:
            client = Client.objects.create(user=self.user)

        self.__client = client
        return client

    def get_checkout_info_context(self) -> dict:
        return {
            'addresses': self.client.addresses.all(),
            'phone': self.user.phone or '',
            'email': self.user.email or '',
            'payment_types': Order.payment_choices,
            'delivery': 1,
        }

    @atomic  # type: ignore
    def create_order(self, cart_service: CartService) -> Order:
        order_data = self._get_order_data(
            CartInfoService.get_product_data(cart_service.cart)
        )
        order = Order.objects.create(**order_data)
        self._set_order_products(order, cart_service.cart)

        self._set_client_info()
        cart_service.delete_all()
        MailService.send_order_mails(order)
        return order

    def _get_order_data(self,
                        products: QuerySet[CartProducts]) -> dict:
        return {
            'employee': self._get_employee(),
            'client': self.client,
            'payment_type': (Order.PaymentChoices.PICKUP
                             if not self.post_data.get('delivery') else
                             self.post_data.get('payment')),
            'total': CartInfoService.calculate_total_price(products),
            'info': self.post_data.get('info')
        }

    @staticmethod
    def _get_employee() -> User:
        return User.objects.filter(
            is_staff=True, is_active=True).order_by('?').first()

    def _set_client_info(self) -> None:
        self.client.user.phone = self.post_data.get('cellphone')
        self.client.user.email = self.post_data.get('email')
        self.client.save()

    @staticmethod
    def _set_order_products(order: Order, cart: Cart) -> None:
        order_products = [OrderProducts(
            product=cart_product.product,
            order=order,
            quantity=cart_product.quantity,
            price=cart_product.price
        ) for cart_product in CartInfoService.get_product_data(cart)]
        OrderProducts.objects.bulk_create(order_products)

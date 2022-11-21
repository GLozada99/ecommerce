from django.db.models import QuerySet
from django.db.transaction import atomic

from ecommerce import settings
from ecommerce.clients.models import Client
from ecommerce.core.models import User
from ecommerce.core.services.mail import MailService
from ecommerce.order.exceptions import NoEmployeeAvailableException
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
            'payment_types': Order.payment_choices,
            'delivery': 1,
        }

    @atomic  # type: ignore
    def create_order(self, cart_service: CartService) -> Order:
        order_data = self._get_order_data(
            CartInfoService.get_product_data(cart_service.cart)
        )
        order = Order.objects.create(**order_data)
        order_products = self._set_order_products(order, cart_service.cart)
        self._set_client_info()
        cart_service.delete_all()
        MailService.send_order_mails(order, order_products)
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
        if user := (User.objects.filter(
                groups__name=settings.GROUPS_EMPLOYEE, is_staff=True,
                is_active=True).order_by('?').first()):
            return user
        else:
            raise NoEmployeeAvailableException

    def _set_client_info(self) -> None:
        user = self.client.user
        data = self.post_data
        user.phone = data.get('cellphone')
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        self.client.user.save(update_fields=['phone', 'first_name',
                                             'last_name'])

    @staticmethod
    def _set_order_products(order: Order, cart: Cart) -> OrderProducts:
        order_products = [OrderProducts(
            product=cart_product.product,
            order=order,
            quantity=cart_product.quantity,
            price=cart_product.price
        ) for cart_product in CartInfoService.get_product_data(cart)]
        return OrderProducts.objects.bulk_create(order_products)

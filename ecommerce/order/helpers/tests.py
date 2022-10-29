import uuid

from faker import Faker

from ecommerce.order.models.cart import Cart
from ecommerce.order.services.cart import CartService


def get_random_cookie_id() -> uuid.UUID:
    return Cart.objects.filter(
        cookie_id__isnull=False).order_by('?').first().cookie_id


def helper_test_add_product(
        service: CartService, product_id: int, qty: int) -> None:
    for _ in range(qty):
        service.add_product(product_id)


def helper_test_remove_product(
        service: CartService, product_id: int, qty: int,
        qty_rem: int) -> None:
    for _ in range(qty):
        service.add_product(product_id)

    for _ in range(qty_rem):
        service.remove_product(product_id)


def helper_test_delete_all_products(
        service: CartService, product_id: int, qty: int) -> None:
    for _ in range(qty):
        service.add_product(product_id)

    service.delete_all()


def get_random_post_data() -> dict:
    faker = Faker()
    return {
        'info': faker.paragraphs(1),
        'cellphone': faker.phone_number(),
        'email': faker.email(),
    }

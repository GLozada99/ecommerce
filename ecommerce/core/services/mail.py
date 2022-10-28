from django.template.loader import render_to_string

from ecommerce.core.models import User
from ecommerce.order.models.order import Order, OrderProducts


class MailService:

    @classmethod
    def send_order_mails(cls, order: Order, products: OrderProducts) -> None:
        cls._send_customer_order_email(order, products)
        cls._send_employee_order_email(order, products)

    @staticmethod
    def send_mail(recipient: User, subject: str,
                  context: dict, template: str) -> None:
        html_message = render_to_string(template, context)
        recipient.email_user(subject, message='', html_message=html_message)

    @classmethod
    def _send_customer_order_email(
            cls, order: Order, products: OrderProducts) -> None:
        subject, context = cls._get_context_subject_order_email(
            order, products
        )
        cls.send_mail(order.client.user, subject, context,
                      'mails/customer_order_email.html')

    @classmethod
    def _send_employee_order_email(
            cls, order: Order, products: OrderProducts) -> None:
        subject, context = cls._get_context_subject_order_email(
            order, products
        )
        cls.send_mail(order.employee, subject, context,
                      'mails/employee_order_email.html')

    @staticmethod
    def _get_context_subject_order_email(
            order: Order, products: OrderProducts) -> tuple[str, dict]:
        return f'Order with ID {order.id}', {'order': order,
                                             'products_data': products}

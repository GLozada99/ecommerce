from django.template.loader import render_to_string

from ecommerce.clients.models import Client
from ecommerce.core.models import User
from ecommerce.order.models.order import Order


class MailService:

    @classmethod
    def send_order_mails(cls, order: Order) -> None:
        cls.send_customer_order_email(order.client, order.employee, order.id)
        cls.send_employee_order_email(order.employee, order.client, order.id)

    @staticmethod
    def send_mail(recipient: User, subject: str,
                  context: dict, template: str) -> None:
        html_message = render_to_string(template, context)
        recipient.email_user(subject, message='', html_message=html_message)

    @classmethod
    def send_customer_order_email(
            cls, client: Client, employee: User, order_id: int) -> None:
        subject = f'Order with ID {order_id}'
        context = {
            'client': client, 'employee': employee,
        }
        cls.send_mail(client.user, subject, context,
                      'mails/customer_order_email.html')

    @classmethod
    def send_employee_order_email(
            cls, employee: User, client: Client, order_id: int) -> None:
        subject = f'Order with ID {order_id}'
        context = {
            'client': client, 'employee': employee,
        }
        cls.send_mail(client.user, subject, context,
                      'mails/employee_order_email.html')

# pylint: disable=missing-module-docstring

from django.core.mail import send_mail as base_send_mail
from django.template.loader import get_template
from .settings import DEFAULT_FROM_EMAIL

def send_mail(
    subject: str,
    message_template: str,
    html_message_template: str,
    recipient_list: list,
    context: dict=None) -> int:

    message = get_template(message_template).render(context)
    html_message = get_template(html_message_template, context).render(context)

    return base_send_mail(
        subject,
        message,
        DEFAULT_FROM_EMAIL,
        recipient_list,
        html_message=html_message
    )

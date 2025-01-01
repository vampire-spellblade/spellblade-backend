# pylint: disable=missing-module-docstring

from django.core.mail import send_mail as base_send_mail
from django.template.loader import get_template
from .settings import DEFAULT_FROM_EMAIL, EMAIL_SUBJECT_PREFIX

def send_mail(
    subject: str,
    message_template: str,
    html_message_template: str,
    recipient_list: list,
    context: dict=None) -> int:
    '''Sends an email to a list of recipients.

    Args:
        subject (str): The subject of the email.
        message_template (str): The template for the plain text message.
        html_message_template (str): The template for the HTML message.
        recipient_list (list): The list of recipients.
        context (dict): The context for the templates.

    Returns:
        int: The number of emails sent successfully.
    '''
    message = get_template(message_template).render(context)
    html_message = get_template(html_message_template, context).render(context)

    return base_send_mail(
        EMAIL_SUBJECT_PREFIX + subject,
        message,
        DEFAULT_FROM_EMAIL,
        recipient_list,
        html_message=html_message
    )

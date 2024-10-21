from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_assignment_email_task(subject, message, recipient_list):
    # Validate recipient_list
    if not isinstance(recipient_list, list) or not recipient_list:
        raise ValueError("recipient_list must be a non-empty list of email addresses")
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )

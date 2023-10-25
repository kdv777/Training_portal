from typing import Dict, Union

from celery import shared_task
from django.core.mail import send_mail

from authapp.models import User


@shared_task
def send_feedback_mail(message_form: Dict[str, Union[int, str]]) -> None:
    user = User.objects.filter(pk=message_form.get("user_id")).first()
    send_mail(
        subject="Training portal  HelpDesk",
        message=message_form["message"],
        from_email=user.email if user else "Help page",
        recipient_list=["helpdesk@training_portal.com"],
        fail_silently=False,
    )

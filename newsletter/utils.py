from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.utils import timezone
from .models import Newsletter, NewsletterSent
from django.contrib.auth import get_user_model

User = get_user_model()

import os
from django.conf import settings
from django.utils import timezone
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To
from .models import Newsletter, NewsletterSent
from django.contrib.auth import get_user_model

User = get_user_model()


def send_newsletter(newsletter_id):
    newsletter = Newsletter.objects.get(id=newsletter_id)
    users = User.objects.filter(is_active=True).exclude(email__isnull=True)

    sg = SendGridAPIClient(settings.SENDGRID_API_KEY)

    for user in users:
        message = Mail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_emails=To(user.email),
            subject=newsletter.title,
            plain_text_content=newsletter.content,
            html_content=f"<html><body>{newsletter.content}</body></html>",
        )

        try:
            response = sg.send(message)
            if 200 <= response.status_code < 300:
                status = "sent"
            else:
                status = "failed"
        except Exception:
            status = "failed"

        NewsletterSent.objects.create(
            newsletter=newsletter,
            recipient=user,
            status=status,
        )

    newsletter.sent_at = timezone.now()
    newsletter.save()

from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class Newsletter(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    sent_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title


class NewsletterSent(models.Model):
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=20,
        choices=[("sent", "Sent"), ("failed", "Failed")],
        default="sent"
    )

    def __str__(self):
        return f"{self.newsletter.title} → {self.recipient.email}"

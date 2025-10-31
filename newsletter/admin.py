from django.contrib import admin, messages
from .models import Newsletter, NewsletterSent
from .utils import send_newsletter


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "sent_at")
    actions = ["send_to_all"]

    def send_to_all(self, request, queryset):
        for newsletter in queryset:
            send_newsletter(newsletter.id)
        self.message_user(request, "Newsletter(s) sent successfully.", messages.SUCCESS)

    

@admin.register(NewsletterSent)
class NewsletterSentAdmin(admin.ModelAdmin):
    list_display = ("newsletter", "recipient", "status", "sent_at")
    list_filter = ("status",)


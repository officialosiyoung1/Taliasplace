from django.contrib import admin
from .models import SMTPSettings, TelegramSettings

@admin.register(SMTPSettings)
class SMTPSettingsAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "webmail_user",
        "smtp_host",
        "smtp_port",
        "security_mode",
        "notification_recipient_email",
        "is_active",
        "updated_at",
    ]
    list_filter = ["is_active", "security_mode"]
    search_fields = ["title", "webmail_user", "smtp_host", "notification_recipient_email"]


@admin.register(TelegramSettings)
class TelegramSettingsAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "chat_id",
        "is_active",
        "notify_on_contact",
        "notify_on_booking",
        "updated_at",
    ]
    list_filter = ["is_active", "notify_on_contact", "notify_on_booking"]
    search_fields = ["title", "chat_id"]

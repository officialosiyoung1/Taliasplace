from django.db import models

class SMTPSettings(models.Model):
    SECURITY_CHOICES = [
        ("SSL", "SSL (Recommended for Port 465)"),
        ("TLS", "TLS (Recommended for Port 587)"),
    ]

    title = models.CharField(
        max_length=100,
        default="cPanel Webmail SMTP",
        help_text="Friendly label for this configuration"
    )
    smtp_host = models.CharField(
        max_length=255,
        default="mail.taliasplace.com",
        help_text="SMTP server host, e.g. mail.yourdomain.com"
    )
    smtp_port = models.IntegerField(
        default=465,
        help_text="SMTP port (usually 465 for SSL or 587 for TLS)"
    )
    security_mode = models.CharField(
        max_length=10,
        choices=SECURITY_CHOICES,
        default="SSL"
    )
    webmail_user = models.CharField(
        max_length=255,
        help_text="Webmail address used for SMTP login, e.g. info@yourdomain.com"
    )
    webmail_password = models.CharField(
        max_length=255,
        help_text="Password for webmail account"
    )
    default_from_email = models.CharField(
        max_length=255,
        blank=True,
        help_text="Sender header, e.g. Talia's Place <info@yourdomain.com>"
    )
    notification_recipient_email = models.EmailField(
        default="perpetualasadueze@gmail.com",
        help_text="Admin email to receive contact messages and booking notifications"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Designate this configuration as active for sending mail"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "SMTP Setting"
        verbose_name_plural = "SMTP Settings"
        ordering = ["-is_active", "-updated_at"]

    def save(self, *args, **kwargs):
        if self.is_active:
            SMTPSettings.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

    def __str__(self):
        status = "Active" if self.is_active else "Inactive"
        return f"{self.title} ({self.webmail_user} @ {self.smtp_host}:{self.smtp_port}) [{status}]"


class TelegramSettings(models.Model):
    title = models.CharField(
        max_length=100,
        default="Talia's Place Alerts Bot",
        help_text="Friendly label for this bot connection"
    )
    bot_token = models.CharField(
        max_length=255,
        help_text="Telegram Bot Token from @BotFather (e.g. 7123456789:AAH...)"
    )
    chat_id = models.CharField(
        max_length=100,
        help_text="Your Telegram Chat ID or Channel ID where alerts should be sent"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Designate this Telegram bot configuration as active"
    )
    notify_on_contact = models.BooleanField(
        default=True,
        help_text="Receive instant notifications for new Contact form inquiries"
    )
    notify_on_booking = models.BooleanField(
        default=True,
        help_text="Receive instant notifications for new BookMe appointments"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Telegram Setting"
        verbose_name_plural = "Telegram Settings"
        ordering = ["-is_active", "-updated_at"]

    def save(self, *args, **kwargs):
        if self.is_active:
            TelegramSettings.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

    def __str__(self):
        status = "Active" if self.is_active else "Inactive"
        return f"{self.title} (Chat: {self.chat_id}) [{status}]"

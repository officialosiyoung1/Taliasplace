import logging
from rest_framework import generics
from .models import ContactMessage
from .serializers import ContactMessageSerializer
from email_settings.services import send_contact_notification
from email_settings.telegram_services import notify_telegram_contact

logger = logging.getLogger(__name__)

class ContactMessageCreateView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

    def perform_create(self, serializer):
        contact_message = serializer.save()

        # Dynamically send email via active cPanel SMTP configuration (safely wrapped)
        try:
            send_contact_notification(contact_message)
        except Exception as exc:
            logger.error(f"Failed to send contact notification email #{contact_message.id}: {exc}", exc_info=True)

        # Dynamically send instant Telegram alert if configured (safely wrapped)
        try:
            notify_telegram_contact(contact_message)
        except Exception as exc:
            logger.error(f"Failed to send contact notification Telegram #{contact_message.id}: {exc}", exc_info=True)

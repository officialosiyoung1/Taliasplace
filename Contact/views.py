from rest_framework import generics
from .models import ContactMessage
from .serializers import ContactMessageSerializer
from email_settings.services import send_contact_notification
from email_settings.telegram_services import notify_telegram_contact

class ContactMessageCreateView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

    def perform_create(self, serializer):
        contact_message = serializer.save()
        # Dynamically send email via active cPanel SMTP configuration
        send_contact_notification(contact_message)
        # Dynamically send instant Telegram alert if configured
        notify_telegram_contact(contact_message)

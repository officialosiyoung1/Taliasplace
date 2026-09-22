from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SMTPSettings, TelegramSettings
from .serializers import SMTPSettingsSerializer, TelegramSettingsSerializer
from .services import test_smtp_handshake, get_active_smtp_config
from .telegram_services import test_telegram_connection, get_active_telegram_config

class SMTPSettingsViewSet(viewsets.ModelViewSet):
    """
    Full CRUD ViewSet for SMTP / Webmail configurations.
    """
    queryset = SMTPSettings.objects.all().order_by("-is_active", "-updated_at")
    serializer_class = SMTPSettingsSerializer
    permission_classes = [AllowAny]


class TestSMTPConnectionView(APIView):
    """
    Endpoint to test SMTP connection and send a verification email.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        setting_id = data.get("id")
        existing = None
        if setting_id:
            existing = SMTPSettings.objects.filter(id=setting_id).first()

        active_fallback = get_active_smtp_config()

        smtp_host = data.get("smtp_host") or getattr(existing, "smtp_host", active_fallback.smtp_host)
        smtp_port = data.get("smtp_port") or getattr(existing, "smtp_port", active_fallback.smtp_port)
        security_mode = data.get("security_mode") or getattr(existing, "security_mode", active_fallback.security_mode)
        webmail_user = data.get("webmail_user") or getattr(existing, "webmail_user", active_fallback.webmail_user)

        submitted_password = data.get("webmail_password")
        if submitted_password and submitted_password != "••••••••":
            webmail_password = submitted_password
        elif existing and existing.webmail_password:
            webmail_password = existing.webmail_password
        else:
            webmail_password = active_fallback.webmail_password

        recipient = (
            data.get("recipient_email")
            or data.get("notification_recipient_email")
            or getattr(existing, "notification_recipient_email", None)
            or active_fallback.notification_recipient_email
        )

        try:
            smtp_port = int(smtp_port)
        except (ValueError, TypeError):
            return Response(
                {"success": False, "message": "Invalid SMTP port number."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not smtp_host or not webmail_user or not webmail_password or not recipient:
            return Response(
                {
                    "success": False,
                    "message": "Missing required SMTP details (Host, Webmail User, Password, and Recipient are required)."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        success, message = test_smtp_handshake(
            host=smtp_host.strip(),
            port=smtp_port,
            security_mode=security_mode,
            username=webmail_user.strip(),
            password=webmail_password.strip(),
            recipient=recipient.strip(),
        )

        status_code = status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST
        return Response({"success": success, "message": message}, status=status_code)


class TelegramSettingsViewSet(viewsets.ModelViewSet):
    """
    Full CRUD ViewSet for Telegram Bot settings.
    """
    queryset = TelegramSettings.objects.all().order_by("-is_active", "-updated_at")
    serializer_class = TelegramSettingsSerializer
    permission_classes = [AllowAny]


class TestTelegramConnectionView(APIView):
    """
    Endpoint to test Telegram Bot connection by sending a verification message.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        setting_id = data.get("id")
        existing = None
        if setting_id:
            existing = TelegramSettings.objects.filter(id=setting_id).first()

        active_fallback = get_active_telegram_config()

        chat_id = data.get("chat_id") or getattr(existing, "chat_id", getattr(active_fallback, "chat_id", ""))

        submitted_token = data.get("bot_token")
        if submitted_token and submitted_token != "••••••••":
            bot_token = submitted_token
        elif existing and existing.bot_token:
            bot_token = existing.bot_token
        elif active_fallback and active_fallback.bot_token:
            bot_token = active_fallback.bot_token
        else:
            bot_token = ""

        if not bot_token or not chat_id:
            return Response(
                {
                    "success": False,
                    "message": "Both Telegram Bot Token and Chat ID are required to test."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        success, message = test_telegram_connection(bot_token, chat_id)
        status_code = status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST
        return Response({"success": success, "message": message}, status=status_code)

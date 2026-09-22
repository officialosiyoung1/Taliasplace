from unittest.mock import patch
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from .models import SMTPSettings, TelegramSettings
from .telegram_services import notify_telegram_contact, notify_telegram_booking, test_telegram_connection
from Contact.models import ContactMessage
from booking.models import Booking


class SMTPSettingsAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.profile = SMTPSettings.objects.create(
            title="cPanel Test",
            smtp_host="mail.example.com",
            smtp_port=465,
            security_mode="SSL",
            webmail_user="info@example.com",
            webmail_password="secretpassword",
            notification_recipient_email="admin@example.com",
            is_active=True,
        )

    def test_list_smtp_settings(self):
        response = self.client.get("/api/email-settings/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["webmail_password"], "••••••••")

    def test_create_smtp_settings(self):
        payload = {
            "title": "Secondary SMTP",
            "smtp_host": "mail.secondary.com",
            "smtp_port": 587,
            "security_mode": "TLS",
            "webmail_user": "support@secondary.com",
            "webmail_password": "newpassword123",
            "notification_recipient_email": "admin@secondary.com",
            "is_active": True,
        }
        response = self.client.post("/api/email-settings/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Secondary SMTP")

        self.profile.refresh_from_db()
        self.assertFalse(self.profile.is_active)

    def test_update_smtp_settings(self):
        update_payload = {
            "smtp_port": 587,
            "security_mode": "TLS",
        }
        response = self.client.patch(f"/api/email-settings/{self.profile.id}/", update_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.smtp_port, 587)
        self.assertEqual(self.profile.security_mode, "TLS")
        self.assertEqual(self.profile.webmail_password, "secretpassword")

    def test_delete_smtp_settings(self):
        response = self.client.delete(f"/api/email-settings/{self.profile.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SMTPSettings.objects.count(), 0)

    def test_test_connection_validation(self):
        response = self.client.post("/api/email-settings/test-connection/", {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TelegramSettingsAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.telegram_profile = TelegramSettings.objects.create(
            title="Primary Telegram",
            bot_token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
            chat_id="987654321",
            is_active=True,
            notify_on_contact=True,
            notify_on_booking=True,
        )

    def test_list_telegram_settings(self):
        response = self.client.get("/api/telegram-settings/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["bot_token"], "••••••••")

    def test_create_telegram_settings(self):
        payload = {
            "title": "Secondary Bot",
            "bot_token": "987654:XYZ-ABC9876",
            "chat_id": "1122334455",
            "is_active": True,
        }
        response = self.client.post("/api/telegram-settings/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Secondary Bot")

        self.telegram_profile.refresh_from_db()
        self.assertFalse(self.telegram_profile.is_active)

    def test_update_telegram_settings(self):
        payload = {
            "chat_id": "999888777",
        }
        response = self.client.patch(f"/api/telegram-settings/{self.telegram_profile.id}/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.telegram_profile.refresh_from_db()
        self.assertEqual(self.telegram_profile.chat_id, "999888777")
        self.assertEqual(self.telegram_profile.bot_token, "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")

    def test_telegram_connection_missing_fields(self):
        response = self.client.post("/api/telegram-settings/test-connection/", {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("email_settings.telegram_services.send_telegram_raw_message")
    def test_test_connection_endpoint_success(self, mock_send):
        mock_send.return_value = (True, {"ok": True})
        payload = {
            "bot_token": "valid_token",
            "chat_id": "123456789",
        }
        response = self.client.post("/api/telegram-settings/test-connection/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        mock_send.assert_called_once()

    @patch("email_settings.telegram_services.send_telegram_raw_message")
    def test_notify_telegram_contact_success(self, mock_send):
        mock_send.return_value = (True, {"ok": True})
        contact = ContactMessage.objects.create(
            name="John & Jane <Doe>",
            email="test@example.com",
            message="Need bridal makeup package <3",
        )
        res = notify_telegram_contact(contact)
        self.assertTrue(res)
        mock_send.assert_called_once()
        sent_token, sent_chat_id, sent_text = mock_send.call_args[0][:3]
        self.assertEqual(sent_token, self.telegram_profile.bot_token)
        self.assertEqual(sent_chat_id, self.telegram_profile.chat_id)
        # Ensure HTML entities are properly escaped
        self.assertIn("&amp;", sent_text)
        self.assertIn("&lt;Doe&gt;", sent_text)
        self.assertIn("&lt;3", sent_text)

    @patch("email_settings.telegram_services.send_telegram_raw_message")
    def test_notify_telegram_booking_success(self, mock_send):
        mock_send.return_value = (True, {"ok": True})
        booking = Booking.objects.create(
            name="Adaora Eze",
            email="adaora@example.com",
            phone="+2348012345678",
            service="bridal",
            date="2026-11-20",
            time="11:30:00",
            appointment_type="studio",
            message="Looking forward to it & please bring lashes <3",
        )
        res = notify_telegram_booking(booking)
        self.assertTrue(res)
        mock_send.assert_called_once()
        sent_token, sent_chat_id, sent_text = mock_send.call_args[0][:3]
        self.assertEqual(sent_token, self.telegram_profile.bot_token)
        self.assertEqual(sent_chat_id, self.telegram_profile.chat_id)
        self.assertIn("Adaora Eze", sent_text)
        self.assertIn("Bridal Makeup", sent_text)
        self.assertIn("&amp;", sent_text)
        self.assertIn("&lt;3", sent_text)

    @patch("email_settings.telegram_services.send_telegram_raw_message")
    def test_notify_disabled_toggles(self, mock_send):
        self.telegram_profile.notify_on_contact = False
        self.telegram_profile.notify_on_booking = False
        self.telegram_profile.save()

        contact = ContactMessage.objects.create(
            name="Test",
            email="test@example.com",
            message="Test msg",
        )
        booking = Booking.objects.create(
            name="Test",
            email="test@example.com",
            phone="123",
            service="bridal",
            date="2026-11-20",
            time="11:30:00",
            appointment_type="studio",
        )

        self.assertFalse(notify_telegram_contact(contact))
        self.assertFalse(notify_telegram_booking(booking))
        mock_send.assert_not_called()

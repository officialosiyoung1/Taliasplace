from datetime import date, timedelta
from unittest.mock import patch
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Booking

class BookingAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.future_date = (date.today() + timedelta(days=7)).strftime("%Y-%m-%d")

    @patch("booking.views.send_booking_notification")
    @patch("booking.views.notify_telegram_booking")
    def test_create_booking_success(self, mock_telegram, mock_email):
        payload = {
            "name": "Amaka Johnson",
            "email": "amaka@example.com",
            "phone": "+2348031234567",
            "service": "bridal",
            "date": self.future_date,
            "time": "10:00:00",
            "appointment_type": "studio",
            "message": "Excited for my bridal session!",
        }
        response = self.client.post("/api/bookings/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
        booking = Booking.objects.first()
        self.assertEqual(booking.name, "Amaka Johnson")
        mock_email.assert_called_once_with(booking)
        mock_telegram.assert_called_once_with(booking)

    def test_create_booking_even_if_notifications_fail(self):
        """
        Verify that even if notifications fail/crash, the booking is created and returns 201.
        """
        payload = {
            "name": "Zainab Bello",
            "email": "zainab@example.com",
            "phone": "+2348098765432",
            "service": "photoshoot",
            "date": self.future_date,
            "time": "12:00:00",
            "appointment_type": "home",
            "message": "Outdoor photoshoot glam",
        }
        response = self.client.post("/api/bookings/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Booking.objects.filter(name="Zainab Bello").exists())

    def test_list_bookings_success(self):
        Booking.objects.create(
            name="Existing Client",
            email="client@example.com",
            phone="08012345678",
            service="natural",
            date=date.today() + timedelta(days=3),
            time="15:00:00",
            appointment_type="studio",
        )
        response = self.client.get("/api/bookings/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_booking_past_date_fails(self):
        past_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        payload = {
            "name": "Past Date Client",
            "email": "past@example.com",
            "phone": "08012345678",
            "service": "full_glam",
            "date": past_date,
            "time": "12:00:00",
            "appointment_type": "studio",
        }
        response = self.client.post("/api/bookings/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("date", response.data)

    def test_health_check_endpoint(self):
        response = self.client.get("/api/health/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("status"), "healthy")
        self.assertEqual(response.data.get("database"), "connected")

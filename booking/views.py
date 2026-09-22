from rest_framework import generics, status
from rest_framework.response import Response

from .models import Booking
from .serializers import BookingSerializer
from email_settings.services import send_booking_notification
from email_settings.telegram_services import notify_telegram_booking

class BookingListCreateView(generics.ListCreateAPIView):
    queryset = Booking.objects.all().order_by("-created_at")
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        booking = serializer.save()
        # Dynamically send email via active cPanel SMTP configuration
        send_booking_notification(booking)
        # Dynamically send instant Telegram alert if configured
        notify_telegram_booking(booking)


class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


# Backward compatibility
CreateBookingView = BookingListCreateView

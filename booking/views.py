from django.conf import settings
from django.core.mail import send_mail

from rest_framework import generics
from rest_framework.response import Response

from .models import Booking
from .serializers import BookingSerializer


class CreateBookingView(generics.CreateAPIView):

    def post(self, request, *args, **kwargs):

        serializer = BookingSerializer(data=request.data)

        if serializer.is_valid():

            booking = serializer.save()

            send_mail(
                subject=f"New Booking Request - {booking.name}",
                message=(
                    f"New appointment request received.\n\n"
                    f"Name: {booking.name}\n"
                    f"Email: {booking.email}\n"
                    f"Phone: {booking.phone}\n"
                    f"Service: {booking.get_service_display()}\n"
                    f"Date: {booking.date}\n"
                    f"Time: {booking.time}\n"
                    f"Appointment Type: "
                    f"{booking.get_appointment_type_display()}\n\n"
                    f"Additional Details:\n"
                    f"{booking.message or 'No additional details provided.'}"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_NOTIFICATION_EMAIL],
                fail_silently=False,
            )

            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)

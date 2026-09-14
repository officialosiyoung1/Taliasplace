from datetime import date

from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "service",
            "date",
            "time",
            "appointment_type",
            "message",
            "status",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "status",
            "created_at",
            "updated_at",
        ]

    def validate_date(self, value):
        if value < date.today():
            raise serializers.ValidationError(
                "Appointment date cannot be in the past."
            )

        return value

    def validate(self, data):
        appointment_date = data.get("date")
        appointment_time = data.get("time")

        existing_booking = Booking.objects.filter(
            date=appointment_date,
            time=appointment_time,
            status="confirmed",
        ).exists()

        if existing_booking:
            raise serializers.ValidationError(
                "This appointment time is already booked. Please choose another date or time."
            )

        return data
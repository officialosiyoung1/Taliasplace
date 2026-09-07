from django.db import models


BOOKING_STATUS_CHOICES = [
    ("pending", "Pending"),
    ("confirmed", "Confirmed"),
    ("cancelled", "Cancelled"),
    ("completed", "Completed"),
]


SERVICE_CHOICES = [
    ("bridal", "Bridal Makeup"),
    ("birthday_events", "Birthday & Events"),
    ("photoshoot", "Photoshoot Makeup"),
    ("natural", "Natural Makeup"),
    ("full_glam", "Full Glam"),
    ("training", "Makeup Training"),
]


APPOINTMENT_TYPE_CHOICES = [
    ("studio", "Studio Appointment"),
    ("home", "Home Service"),
]


class Booking(models.Model):

    name = models.CharField(max_length=150)

    email = models.EmailField()

    phone = models.CharField(max_length=30)

    service = models.CharField(
        max_length=50,
        choices=SERVICE_CHOICES
    )

    date = models.DateField()

    time = models.TimeField()

    appointment_type = models.CharField(
        max_length=20,
        choices=APPOINTMENT_TYPE_CHOICES
    )

    message = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=BOOKING_STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.service} - {self.date}"
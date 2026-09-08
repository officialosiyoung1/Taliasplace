
from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "service",
        "date",
        "time",
        "appointment_type",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "service",
        "appointment_type",
        "date",
    )

    search_fields = (
        "name",
        "email",
        "phone",
    )

    ordering = ("-created_at",)
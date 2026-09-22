"""
URL configuration for django_project project.
"""
from django.contrib import admin
from django.urls import path, include
from .views import health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/health/", health_check, name="health_check"),
    path("users/", include("Users.urls")),
    path("makeup-product/", include("makeupProduct.urls")),   
    path("api/bookings/", include("booking.urls")),
    path("api/contact/", include("Contact.urls")),
    path("api/email-settings/", include("email_settings.urls")),
    path("api/telegram-settings/", include("email_settings.telegram_urls")),
]

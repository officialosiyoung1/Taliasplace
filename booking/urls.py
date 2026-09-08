from django.urls import path
from .views import BookingCreateView, CreateBookingView


urlpatterns = [
    path("", BookingCreateView.as_view(), name="booking-create"),
    path("create-booking/", CreateBookingView.as_view(), name="booking-create"),
]
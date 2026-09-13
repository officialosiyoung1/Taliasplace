from django.urls import path
from .views import CreateBookingView


urlpatterns = [
    path("", CreateBookingView.as_view(), name="booking-create"),
    path("create-booking/", CreateBookingView.as_view(), name="create-booking"),
]
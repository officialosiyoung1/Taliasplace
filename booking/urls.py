from django.urls import path
from .views import BookingListCreateView, BookingDetailView

urlpatterns = [
    path("", BookingListCreateView.as_view(), name="booking-list-create"),
    path("<int:pk>/", BookingDetailView.as_view(), name="booking-detail"),
    path("<int:pk>", BookingDetailView.as_view(), name="booking-detail-no-slash"),
    path("create-booking/", BookingListCreateView.as_view(), name="create-booking"),
]

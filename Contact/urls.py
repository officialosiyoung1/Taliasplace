from django.urls import path
from .views import ContactMessageCreateView


urlpatterns = [
    path(
        "send-message/",
        ContactMessageCreateView.as_view(),
        name="contact-send-message",
    ),
]
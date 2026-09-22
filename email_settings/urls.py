from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    SMTPSettingsViewSet,
    TestSMTPConnectionView,
    TelegramSettingsViewSet,
    TestTelegramConnectionView,
)

router = DefaultRouter()
router.register(r'telegram', TelegramSettingsViewSet, basename='telegram-settings')
router.register(r'', SMTPSettingsViewSet, basename='email-settings')

urlpatterns = [
    path('test-connection/', TestSMTPConnectionView.as_view(), name='test-smtp-connection'),
    path('telegram/test-connection/', TestTelegramConnectionView.as_view(), name='test-telegram-connection'),
    path('', include(router.urls)),
]

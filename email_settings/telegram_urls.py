from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TelegramSettingsViewSet, TestTelegramConnectionView

router = DefaultRouter()
router.register(r'', TelegramSettingsViewSet, basename='telegram-direct-settings')

urlpatterns = [
    path('test-connection/', TestTelegramConnectionView.as_view(), name='test-telegram-direct-connection'),
    path('', include(router.urls)),
]

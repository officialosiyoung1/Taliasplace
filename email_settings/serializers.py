from rest_framework import serializers
from .models import SMTPSettings, TelegramSettings

class SMTPSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMTPSettings
        fields = [
            "id",
            "title",
            "smtp_host",
            "smtp_port",
            "security_mode",
            "webmail_user",
            "webmail_password",
            "default_from_email",
            "notification_recipient_email",
            "is_active",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "webmail_password": {"write_only": False, "required": False},
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data.get("webmail_password"):
            data["webmail_password"] = "••••••••"
        return data

    def create(self, validated_data):
        if not validated_data.get("default_from_email"):
            user = validated_data.get("webmail_user", "")
            validated_data["default_from_email"] = f"Talia's Place <{user}>" if user else ""
        return super().create(validated_data)

    def update(self, instance, validated_data):
        pwd = validated_data.get("webmail_password")
        if not pwd or pwd == "••••••••":
            validated_data.pop("webmail_password", None)

        if "default_from_email" in validated_data and not validated_data["default_from_email"]:
            user = validated_data.get("webmail_user", instance.webmail_user)
            validated_data["default_from_email"] = f"Talia's Place <{user}>"

        return super().update(instance, validated_data)


class TelegramSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramSettings
        fields = [
            "id",
            "title",
            "bot_token",
            "chat_id",
            "is_active",
            "notify_on_contact",
            "notify_on_booking",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "bot_token": {"write_only": False, "required": False},
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data.get("bot_token"):
            data["bot_token"] = "••••••••"
        return data

    def update(self, instance, validated_data):
        token = validated_data.get("bot_token")
        if not token or token == "••••••••":
            validated_data.pop("bot_token", None)
        return super().update(instance, validated_data)

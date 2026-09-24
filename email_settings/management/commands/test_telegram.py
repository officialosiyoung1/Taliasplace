from django.core.management.base import BaseCommand
from email_settings.telegram_services import get_active_telegram_config, test_telegram_connection

class Command(BaseCommand):
    help = "Test the active Telegram bot connection by sending a verification alert."

    def add_arguments(self, parser):
        parser.add_argument(
            "--token",
            type=str,
            help="Telegram Bot Token (defaults to active database config or TELEGRAM_BOT_TOKEN env)",
        )
        parser.add_argument(
            "--chat-id",
            type=str,
            help="Destination Telegram Chat ID (defaults to active database config or TELEGRAM_CHAT_ID env)",
        )

    def handle(self, *args, **options):
        config = get_active_telegram_config()
        token = options.get("token") or (config.bot_token if config else None)
        chat_id = options.get("chat_id") or (config.chat_id if config else None)

        if not token or not chat_id:
            self.stdout.write(self.style.ERROR(
                "❌ Missing Telegram credentials. Please set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env "
                "or pass --token and --chat-id flags."
            ))
            return

        self.stdout.write(f"Testing Telegram connection to chat ID: {chat_id}...")
        success, message = test_telegram_connection(token, chat_id)

        if success:
            self.stdout.write(self.style.SUCCESS(f"✅ {message}"))
        else:
            self.stdout.write(self.style.ERROR(f"❌ {message}"))

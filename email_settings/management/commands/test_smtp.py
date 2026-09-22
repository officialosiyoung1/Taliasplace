from django.core.management.base import BaseCommand
from email_settings.services import get_active_smtp_config, test_smtp_handshake

class Command(BaseCommand):
    help = "Test the active cPanel SMTP connection by sending a verification email."

    def add_arguments(self, parser):
        parser.add_argument(
            "--recipient",
            type=str,
            help="Destination email address (defaults to configured notification email)",
        )

    def handle(self, *args, **options):
        config = get_active_smtp_config()
        recipient = options.get("recipient") or config.notification_recipient_email

        self.stdout.write(f"Testing SMTP connection to: {config.smtp_host}:{config.smtp_port} ({config.security_mode})...")
        self.stdout.write(f"Using webmail user: {config.webmail_user}")
        self.stdout.write(f"Sending test email to: {recipient}")

        success, message = test_smtp_handshake(
            host=config.smtp_host,
            port=config.smtp_port,
            security_mode=config.security_mode,
            username=config.webmail_user,
            password=config.webmail_password,
            recipient=recipient,
        )

        if success:
            self.stdout.write(self.style.SUCCESS(f"✅ {message}"))
        else:
            self.stdout.write(self.style.ERROR(f"❌ {message}"))

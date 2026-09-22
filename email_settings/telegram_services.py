import html
import json
import logging
import urllib.request
import urllib.error

from .models import TelegramSettings

logger = logging.getLogger(__name__)

def get_active_telegram_config():
    """
    Returns active TelegramSettings profile from database if present and active.
    """
    return TelegramSettings.objects.filter(is_active=True).first()


def send_telegram_raw_message(bot_token, chat_id, text, parse_mode="HTML"):
    """
    Sends an HTTP POST request to Telegram's sendMessage API.
    Returns (success: bool, response_or_error: dict/str).
    """
    clean_token = bot_token.strip()
    clean_chat_id = str(chat_id).strip()
    url = f"https://api.telegram.org/bot{clean_token}/sendMessage"

    payload = {
        "chat_id": clean_chat_id,
        "text": text,
        "parse_mode": parse_mode,
        "disable_web_page_preview": True,
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode("utf-8"))
            if result.get("ok"):
                return True, result
            return False, result.get("description", "Unknown Telegram error")
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8")
        try:
            parsed = json.loads(error_body)
            desc = parsed.get("description", str(exc))
        except Exception:
            desc = error_body or str(exc)
        logger.error(f"Telegram HTTPError: {desc}")
        return False, desc
    except Exception as exc:
        logger.error(f"Telegram connection error: {exc}", exc_info=True)
        return False, str(exc)


def test_telegram_connection(bot_token, chat_id):
    """
    Test Telegram bot connection by sending a verification ping.
    Returns (success: bool, message: str).
    """
    if not bot_token or not chat_id:
        return False, "Bot token and Chat ID are both required."

    text = (
        "🎉 <b>Telegram Bot Connected! — Talia's Place</b>\n\n"
        "Your Telegram alert system is linked and verified.\n\n"
        "✨ You will now receive instant notifications right here whenever a client submits a "
        "<b>Contact Inquiry</b> or <b>BookMe Appointment</b>."
    )

    success, result = send_telegram_raw_message(bot_token, chat_id, text)
    if success:
        return True, "Verification message delivered to your Telegram chat successfully!"
    return False, f"Telegram API error: {result}"


def notify_telegram_contact(contact_instance):
    """
    Sends an instant Telegram notification for a new Contact Message.
    """
    config = get_active_telegram_config()
    if not config or not config.notify_on_contact or not config.bot_token or not config.chat_id:
        return False

    name = html.escape(str(contact_instance.name or ''))
    email = html.escape(str(contact_instance.email or ''))
    message = html.escape(str(contact_instance.message or ''))

    text = (
        "💌 <b>New Website Message — Talia's Place</b>\n\n"
        f"👤 <b>Client:</b> {name}\n"
        f"📧 <b>Email:</b> {email}\n\n"
        f"💬 <b>Message:</b>\n{message}\n"
    )

    try:
        success, _ = send_telegram_raw_message(config.bot_token, config.chat_id, text)
        return success
    except Exception as exc:
        logger.error(f"Failed to send Telegram contact alert: {exc}", exc_info=True)
        return False


def notify_telegram_booking(booking_instance):
    """
    Sends an instant Telegram notification for a new BookMe appointment.
    """
    config = get_active_telegram_config()
    if not config or not config.notify_on_booking or not config.bot_token or not config.chat_id:
        return False

    service_name = html.escape(str(getattr(booking_instance, "get_service_display", lambda: booking_instance.service)()))
    apt_type = html.escape(str(getattr(booking_instance, "get_appointment_type_display", lambda: booking_instance.appointment_type)()))
    client_name = html.escape(str(booking_instance.name or ''))
    phone = html.escape(str(booking_instance.phone or ''))
    email = html.escape(str(booking_instance.email or ''))
    date = html.escape(str(booking_instance.date or ''))
    time = html.escape(str(booking_instance.time or ''))

    text = (
        "✨ <b>New Appointment Booking! — Talia's Place</b>\n\n"
        f"💄 <b>Service:</b> {service_name}\n"
        f"👤 <b>Client:</b> {client_name}\n"
        f"📞 <b>Phone:</b> {phone}\n"
        f"📧 <b>Email:</b> {email}\n"
        f"📅 <b>Date:</b> {date}\n"
        f"⏰ <b>Time:</b> {time}\n"
        f"📍 <b>Type:</b> {apt_type}\n"
    )

    if booking_instance.message:
        escaped_notes = html.escape(str(booking_instance.message))
        text += f"\n📝 <b>Notes:</b>\n{escaped_notes}\n"

    try:
        success, _ = send_telegram_raw_message(config.bot_token, config.chat_id, text)
        return success
    except Exception as exc:
        logger.error(f"Failed to send Telegram booking alert: {exc}", exc_info=True)
        return False

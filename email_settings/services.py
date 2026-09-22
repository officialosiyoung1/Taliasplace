import logging
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.mail.backends.smtp import EmailBackend

from .models import SMTPSettings

logger = logging.getLogger(__name__)

def get_active_smtp_config():
    """
    Retrieve active SMTPSettings from database.
    If none exists, create and return a fallback object based on settings.py / .env.
    """
    config = SMTPSettings.objects.filter(is_active=True).first()
    if config:
        return config

    # Fallback to settings.py
    class FallbackConfig:
        smtp_host = getattr(settings, "EMAIL_HOST", "mail.taliasplace.com")
        smtp_port = getattr(settings, "EMAIL_PORT", 465)
        security_mode = "SSL" if getattr(settings, "EMAIL_USE_SSL", True) else "TLS"
        webmail_user = getattr(settings, "EMAIL_HOST_USER", "")
        webmail_password = getattr(settings, "EMAIL_HOST_PASSWORD", "")
        default_from_email = getattr(settings, "DEFAULT_FROM_EMAIL", webmail_user)
        notification_recipient_email = getattr(
            settings, "CONTACT_NOTIFICATION_EMAIL", "perpetualasadueze@gmail.com"
        )
    return FallbackConfig()


def get_backend_for_config(config):
    """
    Instantiate a Django SMTP EmailBackend dynamically using the given configuration.
    """
    use_ssl = (config.security_mode == "SSL")
    use_tls = (config.security_mode == "TLS")

    return EmailBackend(
        host=config.smtp_host,
        port=config.smtp_port,
        username=config.webmail_user,
        password=config.webmail_password,
        use_ssl=use_ssl,
        use_tls=use_tls,
        timeout=10,
        fail_silently=False,
    )


def test_smtp_handshake(host, port, security_mode, username, password, recipient):
    """
    Test SMTP connection and send a verification test message.
    Returns (success: bool, message: str).
    """
    use_ssl = (security_mode == "SSL")
    use_tls = (security_mode == "TLS")

    backend = EmailBackend(
        host=host,
        port=port,
        username=username,
        password=password,
        use_ssl=use_ssl,
        use_tls=use_tls,
        timeout=10,
        fail_silently=False,
    )

    try:
        # First test open connection
        backend.open()

        # Send test verification email
        subject = "✅ SMTP Verification Test - Talia's Place"
        text_content = (
            "Congratulations! Your cPanel Webmail SMTP configuration is working perfectly.\n\n"
            f"Host: {host}\n"
            f"Port: {port} ({security_mode})\n"
            f"Webmail: {username}\n"
            f"Recipient: {recipient}\n\n"
            "Form submissions from your website will be successfully delivered to this email."
        )
        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 24px; border: 1px solid #e5e7eb; border-radius: 16px; background-color: #ffffff;">
            <div style="text-align: center; padding-bottom: 20px; border-bottom: 1px solid #f3f4f6;">
                <h2 style="color: #ec4899; margin: 0; font-size: 24px;">Talia's Place</h2>
                <p style="color: #6b7280; font-size: 14px; margin-top: 4px;">cPanel Webmail SMTP Verification</p>
            </div>
            <div style="padding: 24px 0;">
                <h3 style="color: #111827; margin-top: 0;">Connection Successful! 🎉</h3>
                <p style="color: #4b5563; font-size: 15px; line-height: 1.6;">
                    Your SMTP credentials have been verified. Inquiries from the Contact form and booking requests from the BookMe form will now be delivered reliably.
                </p>
                <div style="background-color: #f9fafb; border-radius: 8px; padding: 16px; margin: 20px 0; font-size: 14px; color: #374151;">
                    <p style="margin: 4px 0;"><strong>SMTP Host:</strong> {host}</p>
                    <p style="margin: 4px 0;"><strong>Port:</strong> {port} ({security_mode})</p>
                    <p style="margin: 4px 0;"><strong>Webmail Account:</strong> {username}</p>
                    <p style="margin: 4px 0;"><strong>Test Destination:</strong> {recipient}</p>
                </div>
            </div>
            <div style="text-align: center; border-top: 1px solid #f3f4f6; padding-top: 16px; font-size: 12px; color: #9ca3af;">
                Talia's Place · Professional Makeup Artistry · Abuja, Nigeria
            </div>
        </div>
        """

        from_email = f"Talia's Place <{username}>"
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=[recipient],
            connection=backend,
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)
        backend.close()

        return True, f"Connection successful! A test email has been sent to {recipient}."
    except Exception as exc:
        logger.error(f"SMTP Test Connection failed: {exc}", exc_info=True)
        return False, f"Connection failed: {str(exc)}"


def send_contact_notification(contact_instance):
    """
    Sends an inquiry email notification to admin whenever a contact message is submitted.
    """
    config = get_active_smtp_config()
    backend = get_backend_for_config(config)

    subject = f"💌 New Contact Message from {contact_instance.name}"
    from_email = config.default_from_email or config.webmail_user
    to_email = config.notification_recipient_email

    text_body = (
        f"You have received a new contact inquiry on Talia's Place:\n\n"
        f"Name: {contact_instance.name}\n"
        f"Email: {contact_instance.email}\n\n"
        f"Message:\n{contact_instance.message}\n"
    )

    html_body = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 24px; border: 1px solid #f3f4f6; border-radius: 16px; background-color: #ffffff;">
        <div style="background-color: #000000; padding: 20px; border-radius: 12px; text-align: center; margin-bottom: 24px;">
            <h2 style="color: #ffffff; margin: 0; font-size: 22px;">Talias<span style="color: #ec4899;">.</span>Place</h2>
            <p style="color: #9ca3af; font-size: 13px; margin: 4px 0 0 0;">New Website Inquiry</p>
        </div>
        
        <h3 style="color: #111827; margin: 0 0 16px 0; font-size: 18px;">Contact Message Details</h3>
        
        <table style="width: 100%; border-collapse: collapse; font-size: 14px; margin-bottom: 20px;">
            <tr style="border-bottom: 1px solid #f3f4f6;">
                <td style="padding: 10px 0; color: #6b7280; width: 120px;"><strong>Client Name:</strong></td>
                <td style="padding: 10px 0; color: #111827; font-weight: 500;">{contact_instance.name}</td>
            </tr>
            <tr style="border-bottom: 1px solid #f3f4f6;">
                <td style="padding: 10px 0; color: #6b7280;"><strong>Email Address:</strong></td>
                <td style="padding: 10px 0;"><a href="mailto:{contact_instance.email}" style="color: #ec4899; text-decoration: none;">{contact_instance.email}</a></td>
            </tr>
        </table>

        <div style="background-color: #f9fafb; border-left: 4px solid #ec4899; padding: 16px; border-radius: 4px; margin-bottom: 24px;">
            <p style="margin: 0 0 8px 0; font-size: 12px; text-transform: uppercase; color: #6b7280; font-weight: 600;">Message Content:</p>
            <p style="margin: 0; color: #374151; font-size: 14px; line-height: 1.6; white-space: pre-wrap;">{contact_instance.message}</p>
        </div>

        <div style="text-align: center; border-top: 1px solid #f3f4f6; padding-top: 16px; font-size: 12px; color: #9ca3af;">
            This email was generated from your website contact form.
        </div>
    </div>
    """

    try:
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=from_email,
            to=[to_email],
            reply_to=[contact_instance.email],
            connection=backend,
        )
        msg.attach_alternative(html_body, "text/html")
        msg.send(fail_silently=False)
        return True
    except Exception as exc:
        logger.error(f"Error sending contact notification email: {exc}", exc_info=True)
        return False


def send_booking_notification(booking_instance):
    """
    Sends an appointment booking alert to admin whenever a BookMe request is submitted.
    """
    config = get_active_smtp_config()
    backend = get_backend_for_config(config)

    service_name = getattr(booking_instance, "get_service_display", lambda: booking_instance.service)()
    apt_type = getattr(booking_instance, "get_appointment_type_display", lambda: booking_instance.appointment_type)()

    subject = f"✨ New Booking Request: {booking_instance.name} - {service_name}"
    from_email = config.default_from_email or config.webmail_user
    to_email = config.notification_recipient_email

    text_body = (
        f"You have received a new appointment booking request on Talia's Place:\n\n"
        f"Client Name: {booking_instance.name}\n"
        f"Email: {booking_instance.email}\n"
        f"Phone: {booking_instance.phone}\n"
        f"Service: {service_name}\n"
        f"Date: {booking_instance.date}\n"
        f"Time: {booking_instance.time}\n"
        f"Appointment Type: {apt_type}\n\n"
        f"Client Notes:\n{booking_instance.message or 'None'}\n"
    )

    html_body = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 24px; border: 1px solid #f3f4f6; border-radius: 16px; background-color: #ffffff;">
        <div style="background-color: #000000; padding: 24px; border-radius: 12px; text-align: center; margin-bottom: 24px;">
            <h2 style="color: #ffffff; margin: 0; font-size: 24px;">Talias<span style="color: #ec4899;">.</span>Place</h2>
            <p style="color: #ec4899; font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 2px; margin: 6px 0 0 0;">New Appointment Booking</p>
        </div>
        
        <div style="margin-bottom: 20px;">
            <span style="display: inline-block; background-color: #fdf2f8; color: #db2777; font-size: 13px; font-weight: 600; padding: 4px 12px; border-radius: 9999px; margin-bottom: 12px;">
                {service_name}
            </span>
            <h3 style="color: #111827; margin: 0; font-size: 20px;">{booking_instance.name}</h3>
        </div>

        <table style="width: 100%; border-collapse: collapse; font-size: 14px; margin-bottom: 24px;">
            <tr style="border-bottom: 1px solid #f3f4f6;">
                <td style="padding: 10px 0; color: #6b7280; width: 140px;"><strong>Client Email:</strong></td>
                <td style="padding: 10px 0;"><a href="mailto:{booking_instance.email}" style="color: #ec4899; text-decoration: none;">{booking_instance.email}</a></td>
            </tr>
            <tr style="border-bottom: 1px solid #f3f4f6;">
                <td style="padding: 10px 0; color: #6b7280;"><strong>Phone Number:</strong></td>
                <td style="padding: 10px 0; color: #111827; font-weight: 500;">
                    <a href="tel:{booking_instance.phone}" style="color: #111827; text-decoration: none;">{booking_instance.phone}</a>
                </td>
            </tr>
            <tr style="border-bottom: 1px solid #f3f4f6;">
                <td style="padding: 10px 0; color: #6b7280;"><strong>Preferred Date:</strong></td>
                <td style="padding: 10px 0; color: #111827; font-weight: 600;">{booking_instance.date}</td>
            </tr>
            <tr style="border-bottom: 1px solid #f3f4f6;">
                <td style="padding: 10px 0; color: #6b7280;"><strong>Preferred Time:</strong></td>
                <td style="padding: 10px 0; color: #111827; font-weight: 600;">{booking_instance.time}</td>
            </tr>
            <tr style="border-bottom: 1px solid #f3f4f6;">
                <td style="padding: 10px 0; color: #6b7280;"><strong>Location / Type:</strong></td>
                <td style="padding: 10px 0; color: #111827;">{apt_type}</td>
            </tr>
        </table>

        {f'''
        <div style="background-color: #f9fafb; border-left: 4px solid #ec4899; padding: 16px; border-radius: 4px; margin-bottom: 24px;">
            <p style="margin: 0 0 8px 0; font-size: 12px; text-transform: uppercase; color: #6b7280; font-weight: 600;">Additional Notes:</p>
            <p style="margin: 0; color: #374151; font-size: 14px; line-height: 1.6;">{booking_instance.message}</p>
        </div>
        ''' if booking_instance.message else ''}

        <div style="background-color: #fdf2f8; border-radius: 12px; padding: 16px; text-align: center; margin-bottom: 20px;">
            <p style="margin: 0; font-size: 13px; color: #9d174d;">
                You can manage or confirm this appointment in your <a href="http://localhost:5173/dashboard" style="color: #db2777; font-weight: 600; text-decoration: underline;">Admin Dashboard</a>.
            </p>
        </div>

        <div style="text-align: center; border-top: 1px solid #f3f4f6; padding-top: 16px; font-size: 12px; color: #9ca3af;">
            Talia's Place · Professional Makeup Artistry · Abuja, Nigeria
        </div>
    </div>
    """

    try:
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=from_email,
            to=[to_email],
            reply_to=[booking_instance.email],
            connection=backend,
        )
        msg.attach_alternative(html_body, "text/html")
        msg.send(fail_silently=False)
        return True
    except Exception as exc:
        logger.error(f"Error sending booking notification email: {exc}", exc_info=True)
        return False

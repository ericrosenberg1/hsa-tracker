import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)

def send_mail_with_template(subject, template, context, to_email):
    """
    Send an email using a template with both HTML and plain text versions.
    
    Args:
        subject (str): Email subject
        template (str): Path to the email template (without .html extension)
        context (dict): Context data for the template
        to_email (str): Recipient email address
    """
    try:
        # Render HTML content
        html_content = render_to_string(f'{template}.html', context)
        # Create plain text content by stripping HTML
        text_content = strip_tags(html_content)

        # Create message container
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = settings.DEFAULT_FROM_EMAIL
        msg['To'] = to_email

        # Add plain-text and HTML parts to the message
        part1 = MIMEText(text_content, 'plain')
        part2 = MIMEText(html_content, 'html')
        msg.attach(part1)
        msg.attach(part2)

        # Send the email using local SMTP
        with smtplib.SMTP('localhost', 25) as server:
            server.send_message(msg)
            
        logger.info(f"Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {str(e)}")
        return False


def send_password_reset_email(user, reset_url):
    """
    Send a password reset email to a user.
    
    Args:
        user: User model instance
        reset_url (str): Password reset URL
    """
    context = {
        'user': user,
        'reset_url': reset_url,
        'site_name': 'HSA Tracker'
    }
    
    return send_mail_with_template(
        subject='Password Reset Request',
        template='users/email/password_reset_email',
        context=context,
        to_email=user.email
    )
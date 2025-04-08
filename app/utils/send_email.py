import smtplib
from email.mime.text import MIMEText

from core import settings
from errors import EmailServiceError


def send_email(recipient, subject, message):
    sender = settings.email.address
    password = settings.email.password
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    try:
        server.login(sender, password)
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = recipient
        server.sendmail(sender, recipient, msg.as_string())
        server.quit()

    except smtplib.SMTPAuthenticationError:
        raise EmailServiceError(
            message="Authentication Error: Check your email and password."
        )
    except smtplib.SMTPException as e:
        raise EmailServiceError(message=f"SMTP error: {e}")
    except Exception as e:
        raise EmailServiceError(message=f"Unexpected error: {e}")

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings

SMTP_SERVER = "p3plzcpnl492197.prod.phx3.secureserver.net"
SMTP_PORT = 587
SMTP_USE_TLS = True
SMTP_USERNAME = settings.EMAIL_HOST_USER
SMTP_PASSWORD = settings.EMAIL_HOST_PASSWORD

def send_verification_code(email, verification_code):
    sender_email = SMTP_USERNAME
    receiver_email = email
    subject = "Email Verification Code"
    body = f"Your verification code is {verification_code}."

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(sender_email, receiver_email, message.as_string())

def send_password_reset_code(email, verification_code):
    sender_email = SMTP_USERNAME
    receiver_email = email
    subject = "Password Reset Code"
    body = f"Your password reset code is {verification_code}."

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(sender_email, receiver_email, message.as_string())

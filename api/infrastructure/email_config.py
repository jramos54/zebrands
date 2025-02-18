import os
from django.core.mail import send_mail

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "apikey" 
DEFAULT_FROM_EMAIL = "test.backend.jrm@gmail.com"

def send_email(to_email, subject, message):
    """Envía un correo electrónico usando SMTP o AWS SES."""
    try:
        print(f"Intentando enviar correo a {to_email} con asunto: {subject}")  
        send_mail(subject, message, EMAIL_HOST_USER, [to_email])
        print("Correo enviado correctamente") 
        return True
    except Exception as e:
        print(f"Error enviando email: {e}") 
        return False
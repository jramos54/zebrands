import os
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class NotificationService:
    """Interfaz abstracta para el envío de notificaciones."""

    def send_email(self, to: str, subject: str, body: str) -> bool:
        """Envía un correo electrónico a un usuario."""
        raise NotImplementedError("Debes implementar este método.")

class EmailService(NotificationService):
    """Implementación del servicio de notificaciones por correo electrónico."""

    def send_email(self, to_email, subject, message):  # 
        """Envía un correo electrónico usando SendGrid API."""
        try:
            print(f"Intentando enviar correo a {to_email} con asunto: {subject}")  # Debug

            email_message = Mail(
                from_email=settings.DEFAULT_FROM_EMAIL,
                to_emails=to_email,
                subject=subject,
                html_content=f"<p>{message}</p>",
            )

            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)  # Y
            response = sg.send(email_message)

            print(f"Correo enviado, código de respuesta: {response.status_code}")  # Debug
            return response.status_code == 202  
        except Exception as e:
            print(f"Error enviando email: {e}")  # Debug
            return False

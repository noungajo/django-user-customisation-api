from django.core.mail import EmailMessage, get_connection
from django.conf import settings

def send_email(subject, body, recipient_email):
    try:
        with get_connection(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS
        ) as connection:
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [recipient_email,]
            email = EmailMessage(subject, body, email_from, recipient_list, connection=connection)
            email.send()
    except Exception as e:
        # Vous pouvez ajouter des opérations de journalisation ici pour enregistrer l'erreur
        # par exemple logger.error(f"Erreur lors de l'envoi de l'e-mail : {str(e)}")

        # Si vous ne souhaitez pas que l'échec de l'e-mail bloque le programme,
        # vous pouvez simplement passer ici sans faire d'action particulière.
        pass


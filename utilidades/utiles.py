import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv



# Cargar las variables de entorno
load_dotenv()

def sendMail(html, asunto, destinatario):
    # Configuración del servidor SMTP
    msg = MIMEMultipart('alternative')
    msg['Subject'] = asunto
    msg['From'] = os.getenv("SMTP_USER")  # Cambiar 'from' a 'From'
    msg['To'] = destinatario
    # Este formato permite enviar el mensaje en formato HTML
    msg.attach(MIMEText(html, 'html'))
    try:
        # Crear una única conexión al servidor SMTP
        server = smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT")))
        server.set_debuglevel(1)
        server.starttls()  # Inicia la conexión segura
        server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASSWORD"))
        server.sendmail(os.getenv("SMTP_USER"), destinatario, msg.as_string())
        server.quit()
        return True
    except smtplib.SMTPException as e:
        print(f"Error al conectar con el servidor SMTP: {e}")
        return False
    except Exception as e:
        print(f"Error inesperado: {e}")
        return False
    
print("SMTP_SERVER:", os.getenv("SMTP_SERVER"))
print("SMTP_PORT:", os.getenv("SMTP_PORT"))
print("SMTP_USER:", os.getenv("SMTP_USER"))
print("SMTP_PASSWORD:", os.getenv("SMTP_PASSWORD"))
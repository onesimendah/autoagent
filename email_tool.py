import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def envoyer_email(destinataire: str, sujet: str, corps: str):
    brevo_login = os.getenv("BREVO_LOGIN")
    brevo_password = os.getenv("BREVO_SMTP_KEY")
    expediteur = os.getenv("GMAIL_USER")

    print(f"Tentative envoi email à: {destinataire}")

    message = MIMEMultipart()
    message["From"] = expediteur
    message["To"] = destinataire
    message["Subject"] = sujet
    message.attach(MIMEText(corps, "plain"))

    try:
        serveur = smtplib.SMTP("smtp-relay.brevo.com", 587)
        serveur.starttls()
        serveur.login(brevo_login, brevo_password)
        serveur.sendmail(expediteur, destinataire, message.as_string())
        serveur.quit()
        print(f"Email envoyé avec succès à: {destinataire}")
        return {"status": "succès", "message": f"Email envoyé à {destinataire}"}
    except Exception as e:
        print(f"ERREUR Brevo: {str(e)}")
        return {"status": "erreur", "message": str(e)}
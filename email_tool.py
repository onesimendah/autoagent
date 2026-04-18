import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def envoyer_email(destinataire: str, sujet: str, corps: str):
    expediteur = os.getenv("GMAIL_USER")
    mot_de_passe = os.getenv("GMAIL_PASSWORD")
    
    message = MIMEMultipart()
    message["From"] = expediteur
    message["To"] = destinataire
    message["Subject"] = sujet
    message.attach(MIMEText(corps, "plain"))
    
    try:
        serveur = smtplib.SMTP("smtp.gmail.com", 587)
        serveur.starttls()
        serveur.login(expediteur, mot_de_passe)
        serveur.sendmail(expediteur, destinataire, message.as_string())
        serveur.quit()
        return {"status": "succès", "message": f"Email envoyé à {destinataire}"}
    except Exception as e:
        return {"status": "erreur", "message": str(e)}
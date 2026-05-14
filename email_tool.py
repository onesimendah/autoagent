import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def envoyer_email(destinataire: str, sujet: str, corps: str):
    expediteur = os.getenv("GMAIL_USER")
    mot_de_passe = os.getenv("GMAIL_PASSWORD")
    
    print(f"Tentative envoi email à: {destinataire}")
    print(f"Expéditeur: {expediteur}")
    print(f"Mot de passe défini: {'Oui' if mot_de_passe else 'NON - VIDE'}")
    
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
        print(f"Email envoyé avec succès à: {destinataire}")
        return {"status": "succès", "message": f"Email envoyé à {destinataire}"}
    except Exception as e:
        print(f"ERREUR SMTP: {str(e)}")
        return {"status": "erreur", "message": str(e)}
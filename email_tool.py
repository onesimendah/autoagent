import resend
import os

resend.api_key = os.getenv("RESEND_API_KEY")

def envoyer_email(destinataire: str, sujet: str, corps: str):
    expediteur = os.getenv("GMAIL_USER")
    
    print(f"Tentative envoi email à: {destinataire}")
    print(f"Expéditeur: {expediteur}")
    
    try:
        params = {
            "from": "AutoAgent <onboarding@resend.dev>",
            "to": [destinataire],
            "subject": sujet,
            "text": corps,
        }
        email = resend.Emails.send(params)
        print(f"Email envoyé avec succès à: {destinataire}")
        return {"status": "succès", "message": f"Email envoyé à {destinataire}"}
    except Exception as e:
        print(f"ERREUR Resend: {str(e)}")
        return {"status": "erreur", "message": str(e)}
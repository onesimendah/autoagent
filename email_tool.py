import requests
import os

def envoyer_email(destinataire: str, sujet: str, corps: str):
    api_key = os.getenv("BREVO_API_KEY")
    expediteur = os.getenv("GMAIL_USER")

    print(f"Tentative envoi email à: {destinataire}")

    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json"
    }
    data = {
        "sender": {"name": "AutoAgent", "email": expediteur},
        "to": [{"email": destinataire}],
        "subject": sujet,
        "textContent": corps
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            print(f"Email envoyé avec succès à: {destinataire}")
            return {"status": "succès", "message": f"Email envoyé à {destinataire}"}
        else:
            print(f"ERREUR Brevo API: {response.text}")
            return {"status": "erreur", "message": response.text}
    except Exception as e:
        print(f"ERREUR: {str(e)}")
        return {"status": "erreur", "message": str(e)}
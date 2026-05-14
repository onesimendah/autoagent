import imaplib
import email
from email.header import decode_header
from email.utils import parseaddr
import os
import json
from email_tool import envoyer_email
from agent_brain import analyser_instruction

EMAILS_TRAITES_FILE = "emails_traites.json"

MOTS_A_IGNORER = ["no-reply", "noreply", "newsletter", "notification", "donotreply", "mailer-daemon", "postmaster"]


def extraire_email(adresse):
    _, email_propre = parseaddr(adresse)
    return email_propre if email_propre else adresse


def charger_emails_traites():
    try:
        with open(EMAILS_TRAITES_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


def sauvegarder_emails_traites(ids):
    with open(EMAILS_TRAITES_FILE, "w") as f:
        json.dump(ids, f)


def surveiller_et_repondre():
    utilisateur = os.getenv("GMAIL_USER")
    mot_de_passe = os.getenv("GMAIL_PASSWORD")
    print(f"Connexion Gmail avec: {utilisateur}")
    emails_traites = charger_emails_traites()

    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(utilisateur, mot_de_passe)
        print("Connexion Gmail réussie")
        mail.select("inbox")

        _, messages = mail.search(None, "UNSEEN")
        ids = messages[0].split()
        print(f"Emails non lus: {len(ids)}")

        nouveaux = 0
        for id_email in ids:
            id_str = id_email.decode()
            if id_str in emails_traites:
                continue

            _, msg_data = mail.fetch(id_email, "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])

            expediteur_brut = msg["From"]
            expediteur = extraire_email(expediteur_brut)

            sujet_raw, encoding = decode_header(msg["Subject"])[0]
            if isinstance(sujet_raw, bytes):
                sujet = sujet_raw.decode(encoding or "utf-8")
            else:
                sujet = sujet_raw

            # Ignorer les emails automatiques
            if any(mot in expediteur.lower() for mot in MOTS_A_IGNORER):
                print(f"Email automatique ignoré: {expediteur}")
                emails_traites.append(id_str)
                continue

            print(f"Traitement email de: {expediteur} | Sujet: {sujet}")

            corps = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        corps = part.get_payload(decode=True).decode()
                        break
            else:
                corps = msg.get_payload(decode=True).decode()

            instruction = f"""Tu es un agent AI qui répond aux emails au nom de l'entreprise.
            
Email reçu de : {expediteur}
Sujet : {sujet}
Message : {corps[:1000]}

Génère une réponse professionnelle, courtoise et adaptée au contenu de ce message.
Réponds UNIQUEMENT en JSON : {{"action": "repondre", "message": "ta réponse ici"}}"""

            resultat = analyser_instruction(instruction)
            print(f"Résultat agent: {resultat}")

            if resultat.get("action") == "réponse":
                corps_reponse = resultat.get("message", "")
            else:
                corps_reponse = (
                    "Bonjour,\n\nNous avons bien reçu votre message "
                    "et nous vous répondrons dans les plus brefs délais.\n\n"
                    "Cordialement,\nAutoAgent"
                )

            envoyer_email(
                destinataire=expediteur,
                sujet="Re: " + sujet,
                corps=corps_reponse
            )
            print(f"Réponse envoyée à: {expediteur}")

            emails_traites.append(id_str)
            nouveaux += 1

        sauvegarder_emails_traites(emails_traites)
        mail.close()
        mail.logout()

        return {"status": "succes", "nouveaux_emails": nouveaux}

    except Exception as e:
        print(f"ERREUR surveillance: {str(e)}")
        return {"status": "erreur", "message": str(e)}
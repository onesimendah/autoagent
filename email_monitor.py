import imaplib
import email
from email.header import decode_header
import os
import json
from email_tool import envoyer_email

EMAILS_TRAITES_FILE = "emails_traites.json"


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
    emails_traites = charger_emails_traites()

    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(utilisateur, mot_de_passe)
        mail.select("inbox")

        _, messages = mail.search(None, "UNSEEN")
        ids = messages[0].split()

        nouveaux = 0
        for id_email in ids:
            id_str = id_email.decode()
            if id_str in emails_traites:
                continue

            _, msg_data = mail.fetch(id_email, "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])

            expediteur = msg["From"]
            sujet_raw, encoding = decode_header(msg["Subject"])[0]
            if isinstance(sujet_raw, bytes):
                sujet = sujet_raw.decode(encoding or "utf-8")
            else:
                sujet = sujet_raw

            corps_reponse = (
                "Bonjour,\n\n"
                "Nous avons bien recu votre message concernant : "
                + sujet
                + "\n\nNous vous repondrons dans les plus brefs delais.\n\n"
                "Cordialement,\nAutoAgent"
            )

            envoyer_email(
                destinataire=expediteur,
                sujet="Re: " + sujet,
                corps=corps_reponse
            )

            emails_traites.append(id_str)
            nouveaux += 1

        sauvegarder_emails_traites(emails_traites)
        mail.close()
        mail.logout()

        return {"status": "succes", "nouveaux_emails": nouveaux}

    except Exception as e:
        return {"status": "erreur", "message": str(e)}
import imaplib
import email
from email.header import decode_header
import os

def lire_emails(nombre=5):
    utilisateur = os.getenv("GMAIL_USER")
    mot_de_passe = os.getenv("GMAIL_PASSWORD")
    
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(utilisateur, mot_de_passe)
        mail.select("inbox")
        
        _, messages = mail.search(None, "ALL")
        ids = messages[0].split()
        ids_recents = ids[-nombre:]
        
        emails = []
        for id_email in reversed(ids_recents):
            _, msg_data = mail.fetch(id_email, "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])
            
            sujet, encoding = decode_header(msg["Subject"])[0]
            if isinstance(sujet, bytes):
                sujet = sujet.decode(encoding or "utf-8")
            
            expediteur = msg["From"]
            corps = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        corps = part.get_payload(decode=True).decode()
                        break
            else:
                corps = msg.get_payload(decode=True).decode()
            
            emails.append({
                "expediteur": expediteur,
                "sujet": sujet,
                "corps": corps[:500]
            })
        
        mail.close()
        mail.logout()
        return {"status": "succès", "emails": emails}
    
    except Exception as e:
        return {"status": "erreur", "message": str(e)}
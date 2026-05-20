from fastapi import FastAPI
from pydantic import BaseModel
from email_tool import envoyer_email
from gmail_reader import lire_emails
from agent_brain import analyser_instruction
from email_monitor import surveiller_et_repondre, charger_bilan, sauvegarder_bilan
from dotenv import load_dotenv
import threading
import time
import json
from datetime import datetime

load_dotenv()

app = FastAPI()

class EmailData(BaseModel):
    destinataire: str
    sujet: str
    corps: str

class Instruction(BaseModel):
    texte: str

def envoyer_bilan():
    bilan = charger_bilan()
    conversations = bilan.get("conversations", [])
    
    if not conversations:
        corps = "Bonjour,\n\nAucun email traité depuis le dernier bilan.\n\nCordialement,\nAutoAgent"
    else:
        liste = "\n".join([
            f"- {c['date']} | De: {c['expediteur']} | Sujet: {c['sujet']}"
            for c in conversations
        ])
        corps = f"""Bonjour,

Voici le bilan de l'agent AutoAgent :

Total emails reçus : {bilan['total_recus']}
Total emails traités : {bilan['total_traites']}

Détail des conversations traitées :
{liste}

Cordialement,
AutoAgent"""

    envoyer_email(
        destinataire="onesimendah1@gmail.com",
        sujet=f"Bilan AutoAgent du {datetime.now().strftime('%d/%m/%Y')}",
        corps=corps
    )
    print("Bilan envoyé")

    # Réinitialiser le bilan après envoi
    sauvegarder_bilan({"total_recus": 0, "total_traites": 0, "conversations": []})


def planificateur():
    while True:
        try:
            print("Surveillance en cours...")
            resultat = surveiller_et_repondre()
            print(f"Résultat surveillance: {resultat}")
        except Exception as e:
            print(f"Erreur planificateur: {e}")
        time.sleep(300)


def planificateur_bilan():
    while True:
        maintenant = datetime.now()
        if maintenant.hour == 6 and maintenant.minute == 0:
            try:
                envoyer_bilan()
            except Exception as e:
                print(f"Erreur bilan: {e}")
        time.sleep(60)


thread = threading.Thread(target=planificateur, daemon=True)
thread.start()

thread_bilan = threading.Thread(target=planificateur_bilan, daemon=True)
thread_bilan.start()

@app.get("/")
def accueil():
    return {"message": "AutoAgent est en ligne et surveille vos emails !"}

@app.post("/email")
def envoyer(data: EmailData):
    return envoyer_email(data.destinataire, data.sujet, data.corps)

@app.get("/emails/lire")
def lire(nombre: int = 5):
    return lire_emails(nombre)

@app.post("/agent")
def agent(instruction: Instruction):
    return analyser_instruction(instruction.texte)

@app.get("/emails/surveiller")
def surveiller():
    return surveiller_et_repondre()

@app.get("/bilan")
def voir_bilan():
    return charger_bilan()

@app.api_route("/ping", methods=["GET", "HEAD"])
def ping():
    return {"status": "alive"}
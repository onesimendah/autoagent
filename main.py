from fastapi import FastAPI
from pydantic import BaseModel
from email_tool import envoyer_email
from gmail_reader import lire_emails
from agent_brain import analyser_instruction
from email_monitor import surveiller_et_repondre
from dotenv import load_dotenv
import threading
import time

load_dotenv()

app = FastAPI()

class EmailData(BaseModel):
    destinataire: str
    sujet: str
    corps: str

class Instruction(BaseModel):
    texte: str

def planificateur():
    while True:
        try:
            surveiller_et_repondre()
        except:
            pass
        time.sleep(300)

thread = threading.Thread(target=planificateur, daemon=True)
thread.start()

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

    @app.get("/ping")
def ping():
    return {"status": "alive"}
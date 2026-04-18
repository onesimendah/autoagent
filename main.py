from fastapi import FastAPI
from pydantic import BaseModel
from email_tool import envoyer_email
from gmail_reader import lire_emails
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class EmailData(BaseModel):
    destinataire: str
    sujet: str
    corps: str

@app.get("/")
def accueil():
    return {"message": "AutoAgent est en ligne !"}

@app.post("/email")
def envoyer(data: EmailData):
    resultat = envoyer_email(data.destinataire, data.sujet, data.corps)
    return resultat

@app.get("/emails/lire")
def lire(nombre: int = 5):
    return lire_emails(nombre)
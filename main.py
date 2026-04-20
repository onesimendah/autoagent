from fastapi import FastAPI
from pydantic import BaseModel
from email_tool import envoyer_email
from gmail_reader import lire_emails
from agent_brain import analyser_instruction
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class EmailData(BaseModel):
    destinataire: str
    sujet: str
    corps: str

class Instruction(BaseModel):
    texte: str

@app.get("/")
def accueil():
    return {"message": "AutoAgent est en ligne !"}

@app.post("/email")
def envoyer(data: EmailData):
    return envoyer_email(data.destinataire, data.sujet, data.corps)

@app.get("/emails/lire")
def lire(nombre: int = 5):
    return lire_emails(nombre)

@app.post("/agent")
def agent(instruction: Instruction):
    return analyser_instruction(instruction.texte)
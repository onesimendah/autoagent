from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Tache(BaseModel):
    instruction: str

@app.get("/")
def accueil():
    return {"message": "AutoAgent est en ligne !"}

@app.post("/executer")
def executer_tache(tache: Tache):
    return {
        "status": "reçu",
        "instruction": tache.instruction,
        "message": "Agent en cours de traitement..."
    }
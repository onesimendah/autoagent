import os
import json
from groq import Groq
from email_tool import envoyer_email

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyser_instruction(instruction: str):
    prompt = f"""Tu es un agent AI autonome. Analyse cette instruction et réponds UNIQUEMENT en JSON.

Instruction: {instruction}

Si l'instruction demande d'envoyer un email, réponds:
{{"action": "envoyer_email", "destinataire": "email@example.com", "sujet": "sujet ici", "corps": "corps ici"}}

Si l'instruction est une question ou conversation normale, réponds:
{{"action": "repondre", "message": "ta réponse ici"}}

Réponds UNIQUEMENT avec le JSON, rien d'autre."""

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    
    texte = response.choices[0].message.content.strip()
    
    try:
        decision = json.loads(texte)
    except:
        return {"status": "erreur", "message": "L'agent n'a pas pu analyser l'instruction"}
    
    if decision.get("action") == "envoyer_email":
        resultat = envoyer_email(
            decision["destinataire"],
            decision["sujet"],
            decision["corps"]
        )
        return {"status": "succès", "action": "email envoyé", "détails": resultat}
    
    elif decision.get("action") == "repondre":
        return {"status": "succès", "action": "réponse", "message": decision["message"]}
    
    return {"status": "erreur", "message": "Action non reconnue"}
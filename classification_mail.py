# classification_mail.py

from groq import Groq
from dotenv import load_dotenv
import json
import os
import re

# Charger variables du .env
load_dotenv()

client = Groq(api_key=os.environ["GROQ_KEY"])


# --- Charger les fichiers externes ---
def load_text_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


CONTEXT = load_text_file("context.txt")
PROMPT_TEMPLATE = load_text_file("prompt.txt")


# --- Nettoyage du JSON renvoyé ---
def clean_json(raw: str) -> str:
    """
    Supprime les backticks, blocs ```json et espaces autour.
    """
    cleaned = re.sub(r"```json|```", "", raw).strip()
    return cleaned


# --- Fonction principale ---
def classify_ticket(subject: str, body: str) -> dict:

    # Construire le prompt final
    prompt = PROMPT_TEMPLATE.replace("{{sujet}}", subject)\
                            .replace("{{contenu}}", body)

    # On ajoute le contexte comme system prompt
    messages = [
        {"role": "system", "content": CONTEXT},
        {"role": "user", "content": prompt}
    ]

    # Appel au modèle
    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages
    )

    # Récupération du contenu
    raw_response = completion.choices[0].message.content.strip()

    # Debug console (utile)
    print("\n===== RÉPONSE GROQ =====")
    print(raw_response)
    print("===== FIN RÉPONSE GROQ =====\n")

    # Nettoyage
    json_text = clean_json(raw_response)

    print("===== JSON NETTOYÉ =====")
    print(json_text)
    print("===== FIN JSON NETTOYÉ =====\n")

    # Conversion en dict Python
    return json.loads(json_text)

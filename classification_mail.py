
# classification_mail.py

from groq import Groq
from dotenv import load_dotenv
import json
import os
import re

# Charger les variables du .env
load_dotenv()

client = Groq(api_key=os.environ["GROQ_KEY"])


def clean_json(text: str) -> str:
    """
    Nettoie la réponse du modèle :
    - enlève les blocs ```json ... ```
    - enlève les ``` tout courts
    - enlève les espaces inutiles
    """
    # Retirer les blocs ```json ... ```
    text = re.sub(r"```json", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```", "", text)

    # Retirer espaces en trop
    return text.strip()


def classify_ticket(subject: str, body: str) -> dict:
    prompt = f"""
    Tu es un classifieur de tickets automatisé.
    Pour le ticket suivant, retourne un JSON strict :

    - categorie ∈ ["Problème technique informatique", "Demande administrative",
                   "Problème d’accès / authentification", "Support utilisateur",
                   "Bug / dysfonctionnement"]

    - urgence ∈ ["Anodine", "Faible", "Modérée", "Élevée", "Critique"]

    - synthese : résumé en une phrase

    Sujet : {subject}
    Message : {body}

    Répond UNIQUEMENT un JSON valide.
    """

    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}]
    )

    content = completion.choices[0].message.content.strip()

    print("\n===== RÉPONSE GROQ =====")
    print(content)
    print("===== FIN RÉPONSE GROQ =====\n")

    # Nettoyer la réponse
    cleaned = clean_json(content)

    # Debug
    print("===== JSON NETTOYÉ =====")
    print(cleaned)
    print("===== FIN JSON NETTOYÉ =====\n")

    # Charger en JSON
    try:
        return json.loads(cleaned)
    except Exception as e:
        print("ERREUR JSON:", e)
        print("Réponse brute était : ", content)
        return {
            "categorie": "Support utilisateur",
            "urgence": "Faible",
            "synthese": "Impossible de parser la réponse du modèle."
        }

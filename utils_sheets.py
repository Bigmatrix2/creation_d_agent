# utils_sheets.py

from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import uuid
from datetime import datetime

# Authentification via service account
creds = Credentials.from_service_account_file(
    "service_account.json",
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)

sheet_service = build("sheets", "v4", credentials=creds)

# ID du Google Sheet
SHEET_ID = "1uRE_SPJW1q1hg5vcuBkc-_AxlBww1O536Z5-dH5oa9k"

# Mapping catégories → nom de feuille
SHEET_TABS = {
    "Problème technique informatique": "Technique",
    "Demande administrative": "Administratif",
    "Problème d’accès / authentification": "Acces",
    "Support utilisateur": "Support",
    "Bug / dysfonctionnement": "Bug",
}

def append_to_sheet(cat, sujet, urgence, synthese):
    sheet_name = SHEET_TABS[cat]

    # Vérifier si les en-têtes existent déjà
    result = sheet_service.spreadsheets().values().get(
        spreadsheetId=SHEET_ID,
        range=f"{sheet_name}!A1:E1"
    ).execute()

    values = result.get("values", [])

    # Ajouter en-têtes si absents
    if not values:
        headers = [["ids_mail", "Sujet", "Urgence", "Synthèse", "date_enregistrement"]]
        sheet_service.spreadsheets().values().append(
            spreadsheetId=SHEET_ID,
            range=f"{sheet_name}!A1:E1",
            valueInputOption="RAW",
            body={"values": headers}
        ).execute()
        print(f"[OK] En-têtes ajoutés dans '{sheet_name}'")

    # Génération automatique
    random_id = str(uuid.uuid4())[:8]  # id court
    today = datetime.now().strftime("%Y/%m/%d")

    # Nouvel enregistrement
    new_row = [[random_id, sujet, urgence, synthese, today]]

    sheet_service.spreadsheets().values().append(
        spreadsheetId=SHEET_ID,
        range=f"{sheet_name}!A:E",
        valueInputOption="RAW",
        body={"values": new_row}
    ).execute()

    print(f"[OK] Ticket ajouté dans '{sheet_name}'")

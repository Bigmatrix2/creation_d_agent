# utils_sheets.py

from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import os

load_dotenv()

SERVICE_ACCOUNT_PATH = os.environ["GOOGLE_SA_PATH"]
SHEET_ID = os.environ["SHEET_ID"]

creds = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_PATH,
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)

sheet_service = build("sheets", "v4", credentials=creds)

SHEET_TABS = {
    "Problème technique informatique": "Technique",
    "Demande administrative": "Administratif",
    "Problème d’accès / authentification": "Acces",
    "Support utilisateur": "Support",
    "Bug / dysfonctionnement": "Bug",
}


def append_to_sheet(cat, sujet, urgence, synthese):
    sheet_name = SHEET_TABS[cat]

    # Lire la première ligne
    result = sheet_service.spreadsheets().values().get(
        spreadsheetId=SHEET_ID,
        range=f"{sheet_name}!A1:C1"
    ).execute()

    values = result.get("values", [])

    # Ajouter les en-têtes si la feuille est vide
    if not values:
        headers = [["Sujet", "Urgence", "Synthèse"]]
        sheet_service.spreadsheets().values().append(
            spreadsheetId=SHEET_ID,
            range=f"{sheet_name}!A1:C1",
            valueInputOption="RAW",
            body={"values": headers}
        ).execute()
        print(f"[OK] En-têtes ajoutés dans '{sheet_name}'")

    # Ajouter le ticket
    new_row = [[sujet, urgence, synthese]]

    sheet_service.spreadsheets().values().append(
        spreadsheetId=SHEET_ID,
        range=f"{sheet_name}!A:C",
        valueInputOption="RAW",
        body={"values": new_row}
    ).execute()

    print(f"[OK] Ticket ajouté dans '{sheet_name}'")

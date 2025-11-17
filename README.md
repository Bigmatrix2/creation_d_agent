# Agent de Traitement Automatique de Tickets E-mail

Ce projet implémente un agent logiciel complet capable de lire des tickets envoyés par e-mail, de les analyser automatiquement grâce à un modèle IA, puis de les classer et de les enregistrer dans un Google Sheets organisé par catégories.  
Il s’agit d’un système de ticketing automatisé, similaire à ceux utilisés dans les environnements professionnels.

---

## 1. Objectifs du projet

L’agent doit :

1. Lire automatiquement les e-mails présents dans une boîte Gmail.
2. Analyser le sujet et le contenu du mail.
3. Classer chaque ticket dans l’une des catégories suivantes :
   - Problème technique informatique  
   - Demande administrative  
   - Problème d’accès / authentification  
   - Support utilisateur  
   - Bug / dysfonctionnement  
4. Déterminer le niveau d’urgence :
   - Critique  
   - Élevée  
   - Modérée  
   - Faible  
   - Anodine  
5. Générer une synthèse courte et professionnelle.
6. Insérer chaque ticket dans l’onglet correspondant d’un Google Sheets.
7. Fonctionner entièrement de manière automatisée sur l’ensemble des 549 e-mails fournis.

---

## 2. Architecture du projet
<img width="790" height="656" alt="image" src="https://github.com/user-attachments/assets/5a335642-9866-49f8-b564-98c2def94aba" />

Cette architecture sépare proprement :

- La logique métier  
- Les appels aux APIs  
- Le prompt IA  
- La configuration  
- Les données sensibles  

---

## 3. Fonctionnement général

### 3.1 Lecture des mails Gmail  
L’authentification se fait via OAuth2 (fichier `credentials.json`).  
Le script :

- Ouvre une fenêtre de navigateur pour autoriser l’accès  
- Récupère jusqu’à 549 mails  
- Décode chaque message (base64)  
- Extrait sujet + contenu  

Fichier impliqué : `utils_gmail.py`

---

### 3.2 Analyse via IA (Groq – GPT OSS 20B)

Chaque ticket est soumis à un prompt construit à partir de :

- `context.txt` : règles de classification  
- `prompt.txt` : structure du message transmis au modèle  

L’IA retourne un JSON strict contenant :

{
"categorie": "",
"urgence": "",
"synthese": ""
}



Un système de nettoyage automatique supprime les blocs Markdown et normalise la réponse afin d’obtenir un JSON valide.

Fichier impliqué : `classification_mail.py`

---

### 3.3 Enregistrement dans Google Sheets

L’agent écrit chaque ticket dans l’onglet correspondant :

| Catégorie IA                         | Feuille Sheets |
|--------------------------------------|----------------|
| Problème technique informatique       | Technique      |
| Demande administrative                | Administratif  |
| Problème d’accès / authentification   | Acces          |
| Support utilisateur                   | Support        |
| Bug / dysfonctionnement               | Bug            |

Avant d’insérer un ticket :

- Le script vérifie si les en-têtes existent  
- Si la feuille est vide → ajout automatique de :  
  `Sujet | Urgence | Synthèse`

Fichier impliqué : `utils_sheets.py`

---

## 4. Installation du projet

### Prérequis
- Python 3.10 ou supérieur  
- pip installé  
- Accès au compte Gmail contenant les tickets  
- Accès au Google Sheet associé  

### Installation des dépendances

## 5. Configuration des accès

### 5.1 Clé Groq – fichier `.env`

Créer un fichier `.env` :
GROQ_KEY=ta_cle_groq

### 5.2 Connexion Gmail : `credentials.json`

Ce fichier est obtenu via Google Cloud (OAuth2).

Il doit être placé à la racine du projet et est ignoré par `.gitignore`.

---

### 5.3 Accès Google Sheets : `service_account.json`

Ce fichier (clé JSON du Service Account Google Cloud) doit :

- être placé à la racine  
- être ajouté comme éditeur sur le Google Sheet  
- être ignoré par Git  

---

## 6. Exécution du script
Lancer le projet : python main.py


Le programme :

1. charge Gmail  
2. lit tous les mails  
3. applique l’analyse IA  
4. nettoie et parse la réponse  
5. insère dans Google Sheets  
6. passe au mail suivant jusqu’au dernier  

Des messages d’état s’affichent dans la console pour suivre l’avancement.

---

## 7. Gestion des erreurs

Le projet inclut :

- Nettoyage automatique des réponses Groq  
- Gestion des erreurs JSON  
- Gestion des retours vides  
- Debug console  
- Vérification préalable des en-têtes Google Sheets  

L’agent peut traiter l’ensemble des 549 emails sans interruption.

---

## 8. Bonnes pratiques appliquées

- Séparation claire par modules  
- Prompt stocké dans des fichiers externes (`context.txt`, `prompt.txt`)  
- Sécurisation des clés via `.env`  
- Fichiers sensibles exclus du dépôt Git  
- Historique Git propre, découpé par commits  
- Nommage professionnel : `feat:`, `fix:`, `docs:`, `chore:`  
- Code robuste, modulaire et maintenable  
- Manipulation correcte des APIs Google  
- Respect strict du format JSON demandé par l’exercice  

---

## 9. Collaboration et versioning

Ce projet est conçu pour être partagé entre plusieurs collaborateurs :

- commits progressifs, clairs et structurés  
- documentation complète  
- organisation facilitant la relecture  
- règles strictes de sécurité  

Le dépôt peut être cloné et réutilisé facilement.

---

## 10. Auteur

Projet réalisé dans le cadre du module d’automatisation de traitement de tickets e-mail par IA.


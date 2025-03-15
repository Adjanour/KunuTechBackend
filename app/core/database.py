import firebase_admin
from firebase_admin import credentials, firestore

# Load Firebase Credentials
cred = credentials.Certificate("app/core/kunutech-34a30-firebase-adminsdk-fbsvc-abcb1021e6.json")
firebase_admin.initialize_app(cred)
# Firestore Database
db = firestore.client()

import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
import base64

# Load the environment variable
encoded_credentials = os.getenv("FIREBASE_CREDENTIALS")

# Decode it
firebase_credentials = json.loads(base64.b64decode(encoded_credentials))

# Initialize Firebase Admin
cred = credentials.Certificate(firebase_credentials)
firebase_admin.initialize_app(cred)

# Firestore Database
db = firestore.client()

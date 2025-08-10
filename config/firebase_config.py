import firebase_admin
from firebase_admin import credentials, firestore
from schemas.project_settings import Settings

settings = Settings()

cred = credentials.Certificate(settings.SERVICE_ACCOUNT_KEY)
firebase_admin.initialize_app(cred)

db = firestore.client()
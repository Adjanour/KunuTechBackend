from fastapi import APIRouter, HTTPException

from app.core.database import db
from app.models import DeviceToken

router = APIRouter()


# Store FCM Token in Firestore
@router.post("/register-token")
async def register_token(data: DeviceToken):
    try:
        db.collection("device_tokens").document(data.uid).set({"token": data.token})
        return {"message": "FCM token saved"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Get FCM Token for a User
@router.get("/get-token/{uid}")
async def get_token(uid: str):
    doc = db.collection("device_tokens").document(uid).get()
    if doc.exists:
        return doc.to_dict()
    else:
        raise HTTPException(status_code=404, detail="FCM token not found")

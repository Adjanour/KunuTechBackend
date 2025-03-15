from fastapi import APIRouter, HTTPException
from firebase_admin import messaging

from app.core.database import db
from app.models import NotificationData
from app.services.notification import send_push_notification

router = APIRouter()

@router.post("/send-notification")
def send_push_notification(uid: str, title: str, body: str, screen: str):
    # Retrieve FCM token from Firestore
    doc = db.collection("device_tokens").document(uid).get()
    if not doc.exists:
        return {"error": "FCM token not found"}

    token = doc.to_dict()["token"]

    # Send notification with deep linking data
    message = messaging.Message(
        notification=messaging.Notification(title=title, body=body),
        data={"screen": screen},  # Deep linking parameter
        token=token
    )

    response = messaging.send(message)
    return {"message": "Notification sent", "response": response}

# Notify collectors when bins are full

def notify_collectors_on_full_bin(bin_id):
    # Query all collectors
    collectors = db.collection("users").where("role", "==", "collector").stream()

    for collector in collectors:
        send_push_notification(collector.id, f"Bin {bin_id} is full!")


# Notify users on disposal milestone
def notify_user_milestone(user_id, milestone):
    send_push_notification(user_id, f"Congrats! You've reached {milestone} points!")

# async def send_notification(data: NotificationData):
#     # Get the FCM Token
#     doc = db.collection("device_tokens").document(data.uid).get()
#     if not doc.exists:
#         raise HTTPException(status_code=404, detail="FCM token not found")
#
#     fcm_token = doc.to_dict()["token"]
#
#     # Create Notification Message
#     message = messaging.Message(
#         notification=messaging.Notification(title=data.title, body=data.body),
#         token=fcm_token
#     )
#
#     # Send Push Notification
#     try:
#         response = messaging.send(message)
#         return {"message": "Notification sent", "response": response}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
#
# import firebase_admin
# from firebase_admin import messaging, firestore
#
# db = firestore.client()
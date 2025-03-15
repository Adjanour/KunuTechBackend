from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from firebase_admin import firestore, storage
import uuid

from app.core.database import db

router = APIRouter()
bucket = storage.bucket("kunu")


@router.post("/send")
async def send_message(
        sender_id: str = Form(...),
        receiver_id: str = Form(...),
        message: str = Form(""),
        image: Optional[UploadFile] = File(None),
):
    try:
        # Validate sender_id and receiver_id
        if not sender_id or not receiver_id:
            raise HTTPException(status_code=400, detail="Sender ID and Receiver ID are required.")

        # Generate a unique message ID
        message_id = str(uuid.uuid4())
        image_url = ""

        # Upload Image to Firebase Storage if provided
        if image:
            # Validate file type (optional)
            allowed_content_types = ["image/jpeg", "image/png", "image/gif"]
            if image.content_type not in allowed_content_types:
                raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG, PNG, and GIF are allowed.")

            # Upload the file to Firebase Storage
            blob = bucket.blob(f"chat_images/{message_id}.{image.content_type.split('/')[-1]}")
            blob.upload_from_file(image.file, content_type=image.content_type)
            blob.make_public()
            image_url = blob.public_url

        # Save message in Firestore
        db.collection("chats").document(message_id).set({
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "message": message,
            "image_url": image_url,
            "timestamp": firestore.SERVER_TIMESTAMP
        })

        return {"message": "Message sent!", "image_url": image_url}

    except HTTPException as http_exc:
        # Re-raise HTTPExceptions for consistent error handling
        raise http_exc

    except Exception as e:
        # Log the error for debugging purposes (optional, requires a logging setup)
        # logger.error(f"Error sending message: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred while sending the message: {str(e)}")

from fastapi import APIRouter, HTTPException

from app.core.database import db

router = APIRouter()


### 🚀 FETCH AVAILABLE COLLECTORS ###
@router.get("/available")
def get_available_collectors():
    collectors_ref = db.collection("users").where("role", "==", "collector").where("available", "==", True).stream()
    collectors = [{**doc.to_dict(), "id": doc.id} for doc in collectors_ref]

    if not collectors:
        raise HTTPException(status_code=404, detail="No available collectors found")

    return {"collectors": collectors}


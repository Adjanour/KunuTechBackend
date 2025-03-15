from datetime import datetime

from fastapi import APIRouter, HTTPException

from app.core.database import db

router = APIRouter()

@router.post("/scan-qr")
async def scan_qr(user_id: str, bin_id: str):
    bin_doc = db.collection("bins").document(bin_id).get()

    if not bin_doc.exists:
        raise HTTPException(status_code=404, detail="Bin not found")

    # Record disposal & reward points
    db.collection("waste_history").add({
        "user_id": user_id,
        "bin_id": bin_id,
        "timestamp": datetime.utcnow(),
    })
    return {"message": "Disposal verified!", "points_earned": 10}

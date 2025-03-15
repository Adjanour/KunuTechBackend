import uuid
from typing import Dict, List
from fastapi import APIRouter, HTTPException
from app.core.database import db
from app.models import BinData, PickupTask
from app.routes.notification import send_push_notification
from app.schemas import BinCreate, BinUpdate
from app.utils import haversine

router = APIRouter()


@router.post("/", status_code=201)
async def create_bin(bin_data: BinCreate):
    try:
        # Generate a new UUID for the bin
        bin_id = str(uuid.uuid4())

        # Store bin data in Firestore
        db.collection("bins").document(bin_id).set({
            "id": bin_id,
            **bin_data.dict()
        })

        return {"id": bin_id, "message": "Bin successfully created"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create bin: {str(e)}")


@router.put("/{bin_id}")
async def update_bin(data: BinUpdate, bin_id: str):
    try:
        # Update bin data in Firestore
        db.collection("bins").document(bin_id).update(data.dict(exclude_unset=True))

        return {"message": "Bin data updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to update bin: {str(e)}")


@router.post("/bins/update")
async def update_bin_fill_level(bin_id: str, fill_level: int):
    try:
        # Update bin status in Firestore
        bin_ref = db.collection("bins").document(bin_id)
        bin_ref.update({"fill_level": fill_level})

        # If bin is full, notify collectors
        if fill_level >= 85:
            collectors_ref = db.collection("collectors").stream()
            for collector in collectors_ref:
                collector_id = collector.id
                send_push_notification(
                    uid=collector_id,
                    title="Full Bin Alert",
                    body=f"Bin {bin_id} is full and needs collection."
                )

        return {"message": "Bin updated successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update bin fill level: {str(e)}")


@router.get("/", response_model=Dict[str, List[Dict]])
async def get_all_bins():
    try:
        # Fetch all documents from the "bins" collection
        bins_ref = db.collection("bins").stream()

        # Convert each document to a dictionary and include its ID
        bins = [
            {"id": bin.id, **bin.to_dict()}
            for bin in bins_ref
        ]

        return {"bins": bins}

    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while fetching bins.")


@router.get("/nearby")
async def get_nearby_bins(lat: float, lon: float, radius: float = 5.0):
    try:
        bins_ref = db.collection("bins").stream()
        nearby_bins = []

        for bin in bins_ref:
            bin_data = bin.to_dict()
            distance = haversine(lat, lon, bin_data["latitude"], bin_data["longitude"])

            if distance <= radius:
                nearby_bins.append({"id": bin.id, **bin_data})

        return {"bins": nearby_bins}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching nearby bins: {str(e)}")


@router.get("/full")
async def get_full_bins():
    try:
        bins_ref = db.collection("bins").where("status", "==", "full").limit(100).stream()
        full_bins = [{"id": bin.id, **bin.to_dict()} for bin in bins_ref]

        return {"full_bins": full_bins}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching full bins: {str(e)}")


@router.post("/assign-pickup")
async def assign_pickup(task: PickupTask):
    try:
        db.collection("tasks").add(task.dict())
        return {"message": "Pickup task assigned!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to assign pickup task: {str(e)}")
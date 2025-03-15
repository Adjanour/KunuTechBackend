from typing import Dict, List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uuid
from firebase_admin import firestore

from app.core.database import db

router = APIRouter()


# Marketplace Item Schema
class MarketplaceItem(BaseModel):
    user_id: str
    title: str
    category: str  # e.g., "Electronics", "Plastics", "Furniture"
    description: str
    condition: str  # e.g., "New", "Used"
    location: dict  # { "lat": 5.6037, "lon": -0.1870 }
    available: bool = True
    image_url: str


@router.post("/item", response_model=Dict[str, str])
async def post_item(item: MarketplaceItem):
    try:
        # Generate a unique ID for the item
        item_id = str(uuid.uuid4())

        # Convert the Pydantic model to a dictionary and add the generated ID
        item_data = {"id": item_id, **item.dict()}

        # Store the item in Firestore using the generated ID as the document ID
        db.collection("marketplace").document(item_id).set(item_data)

        return {"message": "Item listed successfully!", "item_id": item_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list item: {str(e)}")


@router.get("/items", response_model=Dict[str, List[Dict]])
async def get_items(limit: int = 100):
    try:
        # Fetch available items with a limit for pagination
        items_ref = db.collection("marketplace").where("available", "==", True).limit(limit).stream()
        items = [{"id": item.id, **item.to_dict()} for item in items_ref]

        return {"items": items}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch items: {str(e)}")


@router.get("/items/{category}", response_model=Dict[str, List[Dict]])
async def get_items_by_category(category: str, limit: int = 100):
    try:
        # Fetch items by category with a limit for pagination
        items_ref = (
            db.collection("marketplace")
            .where("category", "==", category)
            .where("available", "==", True)
            .limit(limit)
            .stream()
        )
        items = [{"id": item.id, **item.to_dict()} for item in items_ref]

        return {"items": items}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch items by category: {str(e)}")


@router.put("/item/{item_id}")
async def update_item_status(item_id: str, available: bool):
    try:
        # Update the availability status of the item
        db.collection("marketplace").document(item_id).update({"available": available})

        return {"message": "Item status updated"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update item status: {str(e)}")
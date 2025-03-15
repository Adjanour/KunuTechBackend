from typing import List, Dict
from fastapi import APIRouter, HTTPException
from app.core.database import db
from app.schemas import UserProfile  # Assuming a Pydantic model for profile validation

router = APIRouter()


@router.post("/profile")
async def save_profile(uid: str, profile_data: UserProfile):
    try:
        # Validate profile data using Pydantic model
        db.collection("users").document(uid).set(profile_data.dict())
        return {"message": "Profile updated"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to update profile: {str(e)}")


@router.get("/profile/{uid}")
async def get_profile(uid: str):
    try:
        doc = db.collection("users").document(uid).get()
        if doc.exists:
            return doc.to_dict()
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch profile: {str(e)}")


@router.get("/{user_id}/history")
async def get_user_history(user_id: str, limit: int = 100):
    try:
        history_ref = (
            db.collection("waste_history")
            .where("user_id", "==", user_id)
            .limit(limit)
            .stream()
        )
        history = [{"id": h.id, **h.to_dict()} for h in history_ref]
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch history: {str(e)}")


@router.get("/{user_id}/goals")
async def get_user_goals(user_id: str):
    try:
        user_ref = db.collection("users").document(user_id)
        user = user_ref.get()

        if not user.exists:
            raise HTTPException(status_code=404, detail="User not found")

        return {"goals": user.to_dict().get("goals", [])}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch goals: {str(e)}")


@router.post("/{user_id}/goals/update")
async def update_goal_progress(user_id: str, goal_id: str, progress: int):
    try:
        user_ref = db.collection("users").document(user_id)
        user = user_ref.get()

        if not user.exists:
            raise HTTPException(status_code=404, detail="User not found")

        goals: List[Dict] = user.to_dict().get("goals", [])
        updated = False

        for goal in goals:
            if goal["id"] == goal_id:
                goal["progress"] = progress
                updated = True

        if not updated:
            raise HTTPException(status_code=404, detail="Goal not found")

        user_ref.update({"goals": goals})
        return {"message": "Goal progress updated"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to update goal progress: {str(e)}")
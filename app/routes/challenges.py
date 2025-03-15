from typing import List, Dict
from fastapi import APIRouter, HTTPException
from firebase_admin import firestore

from app.core.database import db

router = APIRouter()


@router.get("/", response_model=Dict[str, List[Dict]])
def get_challenges(limit: int = 100):
    """
    Fetch all available community challenges with pagination.
    """
    try:
        challenges_ref = db.collection("challenges").limit(limit).stream()
        challenges = [{"id": doc.id, **doc.to_dict()} for doc in challenges_ref]

        return {"challenges": challenges}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch challenges: {str(e)}")


@router.post("/join/{user_id}/{challenge_id}")
def join_challenge(user_id: str, challenge_id: str):
    """
    Allow a user to join a specific challenge.
    """
    try:
        # Check if the user exists
        user_ref = db.collection("users").document(user_id)
        user = user_ref.get()

        if not user.exists:
            raise HTTPException(status_code=404, detail="User not found")

        # Check if the challenge exists
        challenge_ref = db.collection("challenges").document(challenge_id)
        challenge = challenge_ref.get()

        if not challenge.exists:
            raise HTTPException(status_code=404, detail="Challenge not found")

        # Add the challenge ID to the user's joined challenges array
        user_ref.update({"joined_challenges": firestore.ArrayUnion([challenge_id])})

        return {"message": "Challenge joined successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to join challenge: {str(e)}")
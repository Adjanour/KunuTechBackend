from fastapi import APIRouter, HTTPException

from app.core.database import db

router = APIRouter()

@router.get("/gamification/{user_id}")
async def get_user_rewards(user_id: str):
    try:
        user_ref = db.collection("users").document(user_id).get()
        user_data = user_ref.to_dict()
        points = user_data.get("points", 0)

        badges = []
        if points >= 100: badges.append("♻️ Eco Newbie")
        if points >= 500: badges.append("🌱 Eco Warrior")
        if points >= 1000: badges.append("🌍 Green Hero")
        if points >= 5000: badges.append("🌟 Sustainability Legend")

        return {"points": points, "badges": badges}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

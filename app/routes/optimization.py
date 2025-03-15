from fastapi import APIRouter
from firebase_admin import firestore
from ..utils import haversine

router = APIRouter()
db = firestore.client()

@router.get("/optimized-route/{collector_id}")
async def optimized_route(collector_id: str):
    """
    Optimize the waste collection route for a given collector.
    """

    # Get collector location
    collector_ref = db.collection("collectors").document(collector_id).get()
    if not collector_ref.exists:
        return {"error": "Collector not found"}
    collector_data = collector_ref.to_dict()
    col_lat, col_lon = collector_data["latitude"], collector_data["longitude"]

    # Get all waste bins
    bins_ref = db.collection("waste_bins").stream()
    bins = [
        {
            "id": bin.id,
            "latitude": bin.to_dict()["latitude"],
            "longitude": bin.to_dict()["longitude"],
            "fill_level": bin.to_dict()["fill_level"],
            "last_collected": bin.to_dict().get("last_collected", ""),
        }
        for bin in bins_ref
    ]

    # Compute distances and sort by priority
    prioritized_bins = sorted(
        bins,
        key=lambda bin: (
            -bin["fill_level"],  # Highest fill level first
            haversine(col_lat, col_lon, bin["latitude"], bin["longitude"])  # Shortest distance
        )
    )

    return {"optimized_route": prioritized_bins}

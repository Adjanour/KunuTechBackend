
from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, List
from datetime import date


# Model for Device Token
class DeviceToken(BaseModel):
    uid: str
    token: str

class NotificationData(BaseModel):
    uid: str
    title: str
    body: str

# Data Model for Smart Bin
class BinData(BaseModel):
    bin_id: str
    latitude: float
    longitude: float
    fill_level: int  # Percentage (0-100)
    status: str  # "full" or "empty"
    binType: str
    last_collected: Optional[str] = None

class Item(BaseModel):
    user_id: str
    title: str
    category: str
    description: str
    condition: str
    location: dict  # {lat, lon}
    available: bool = True

class PickupTask(BaseModel):
    collector_id: str
    bin_id: str


class Goal(BaseModel):
    """
    Represents a user goal.
    """
    id: str = Field(..., description="Unique identifier for the goal")
    title: str = Field(..., description="Title of the goal")
    target: int = Field(..., description="Target value for the goal (e.g., 100kg of waste recycled)")
    progress: int = Field(0, description="Current progress toward the goal")
    start_date: Optional[date] = Field(None, description="Start date of the goal")
    end_date: Optional[date] = Field(None, description="End date of the goal")

    @validator("progress")
    def validate_progress(cls, value, values):
        """
        Ensure progress does not exceed the target.
        """
        if "target" in values and value > values["target"]:
            raise ValueError("Progress cannot exceed the target value.")
        return value


class UserProfile(BaseModel):
    """
    Represents the structure of a user's profile.
    """
    display_name: str = Field(..., description="User's display name")
    email: EmailStr = Field(..., description="User's email address")
    phone_number: Optional[str] = Field(None, description="User's phone number")
    address: Optional[str] = Field(None, description="User's physical address")
    bio: Optional[str] = Field(None, description="A short bio about the user")
    goals: Optional[List[Goal]] = Field(default_factory=list, description="List of user goals")
    created_at: Optional[date] = Field(None, description="Date the profile was created")
    updated_at: Optional[date] = Field(None, description="Date the profile was last updated")

    class Config:
        schema_extra = {
            "example": {
                "display_name": "John Doe",
                "email": "johndoe@example.com",
                "phone_number": "+1234567890",
                "address": "123 Main St, City, Country",
                "bio": "I am passionate about recycling and sustainability.",
                "goals": [
                    {
                        "id": "goal1",
                        "title": "Recycle 100kg of plastic",
                        "target": 100,
                        "progress": 25,
                        "start_date": "2023-01-01",
                        "end_date": "2023-12-31"
                    }
                ],
                "created_at": "2023-01-01",
                "updated_at": "2023-10-01"
            }
        }
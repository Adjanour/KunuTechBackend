from datetime import date
from typing import Optional, List


from pydantic import BaseModel, EmailStr,Field

from app.models import Goal


class BinCreate(BaseModel):
    latitude: float
    longitude: float
    fill_level: int
    status: str

class BinUpdate(BaseModel):
    fill_level: int
    status: str

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
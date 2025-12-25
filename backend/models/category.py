from pydantic import BaseModel, Field
from typing import Literal
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info=None):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)


class Category(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(..., min_length=1, max_length=100)
    type: Literal["expense", "revenue", "cogs"] = Field(...)
    color: str = Field(..., pattern=r"^#[0-9A-Fa-f]{6}$")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "name": "Inventory - Food & Supplies",
                "type": "cogs",
                "color": "#3b82f6"
            }
        }


class CategoryResponse(BaseModel):
    id: str
    name: str
    type: str
    color: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": "507f1f77bcf86cd799439013",
                "name": "Inventory - Food & Supplies",
                "type": "cogs",
                "color": "#3b82f6"
            }
        }
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from bson import ObjectId

from auth.dependencies import get_current_user
from models.user import UserInDB
from models.category import CategoryResponse
import database

router = APIRouter(prefix="/api/v1/categories", tags=["categories"])


@router.get("", response_model=dict)
async def get_categories(current_user: UserInDB = Depends(get_current_user)):
    """
    Get all available transaction categories.
    
    Returns a list of all categories with their id, name, type, and color.
    """
    db = database.get_database()
    categories_collection = db.categories
    
    # Fetch all categories
    categories_cursor = categories_collection.find({})
    categories = await categories_cursor.to_list(length=None)
    
    # Convert to response format
    category_list = []
    for cat in categories:
        category_list.append({
            "id": str(cat["_id"]),
            "name": cat["name"],
            "type": cat["type"],
            "color": cat["color"]
        })
    
    return {"categories": category_list}
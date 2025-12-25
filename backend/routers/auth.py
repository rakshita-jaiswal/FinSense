"""Authentication routes."""
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from passlib.hash import argon2
from bson import ObjectId
from pydantic import BaseModel, EmailStr

from models.user import UserCreate, UserResponse, UserInDB, UserUpdate
from auth.jwt import create_access_token
from auth.dependencies import get_current_user
from database import get_database


router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


class LoginRequest(BaseModel):
    """Login request schema."""
    email: EmailStr
    password: str


@router.post("/signup", response_model=dict, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate):
    """Register a new user account."""
    db = get_database()
    
    # Check if user already exists
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password
    password_hash = argon2.hash(user_data.password)
    
    # Create user document
    user_doc = {
        "email": user_data.email,
        "password_hash": password_hash,
        "first_name": user_data.first_name,
        "last_name": user_data.last_name,
        "business_name": user_data.business_name,
        "phone": user_data.phone,
        "industry": user_data.industry,
        "employees": user_data.employees,
        "monthly_revenue": user_data.monthly_revenue,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    # Insert user into database
    result = await db.users.insert_one(user_doc)
    user_id = str(result.inserted_id)
    
    # Create default subscription (free plan)
    subscription_doc = {
        "user_id": result.inserted_id,
        "is_trial_active": False,
        "trial_started_at": None,
        "trial_ends_at": None,
        "plan": "free",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    await db.subscriptions.insert_one(subscription_doc)
    
    # Create JWT token
    token = create_access_token(data={"sub": user_id})
    
    # Return user and token
    return {
        "access_token": token,
        "user": {
            "id": user_id,
            "email": user_data.email,
            "first_name": user_data.first_name,
            "last_name": user_data.last_name,
            "business_name": user_data.business_name,
            "phone": user_data.phone,
            "industry": user_data.industry,
            "employees": user_data.employees,
            "monthly_revenue": user_data.monthly_revenue
        }
    }


@router.post("/login", response_model=dict)
async def login(login_data: LoginRequest):
    """Authenticate existing user."""
    db = get_database()
    
    # Find user by email
    user_doc = await db.users.find_one({"email": login_data.email})
    if not user_doc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not argon2.verify(login_data.password, user_doc["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create JWT token
    user_id = str(user_doc["_id"])
    token = create_access_token(data={"sub": user_id})
    
    # Return user and token
    return {
        "access_token": token,
        "user": {
            "id": user_id,
            "email": user_doc["email"],
            "first_name": user_doc["first_name"],
            "last_name": user_doc["last_name"],
            "business_name": user_doc["business_name"],
            "phone": user_doc.get("phone"),
            "industry": user_doc.get("industry"),
            "employees": user_doc.get("employees"),
            "monthly_revenue": user_doc.get("monthly_revenue")
        }
    }


@router.post("/logout", response_model=dict)
async def logout(current_user: UserInDB = Depends(get_current_user)):
    """Logout user (token invalidation handled client-side)."""
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=dict)
async def get_current_user_profile(current_user: UserInDB = Depends(get_current_user)):
    """Get current user profile."""
    return {
        "user": {
            "id": str(current_user.id),
            "email": current_user.email,
            "first_name": current_user.first_name,
            "last_name": current_user.last_name,
            "business_name": current_user.business_name,
            "phone": current_user.phone,
            "industry": current_user.industry,
            "employees": current_user.employees,
            "monthly_revenue": current_user.monthly_revenue
        }
    }


@router.put("/profile", response_model=dict)
async def update_profile(
    updates: UserUpdate,
    current_user: UserInDB = Depends(get_current_user)
):
    """Update user profile."""
    db = get_database()
    
    # Build update document (only include provided fields)
    update_doc = {"updated_at": datetime.utcnow()}
    
    if updates.first_name is not None:
        update_doc["first_name"] = updates.first_name
    if updates.last_name is not None:
        update_doc["last_name"] = updates.last_name
    if updates.business_name is not None:
        update_doc["business_name"] = updates.business_name
    if updates.phone is not None:
        update_doc["phone"] = updates.phone
    if updates.industry is not None:
        update_doc["industry"] = updates.industry
    if updates.employees is not None:
        update_doc["employees"] = updates.employees
    if updates.monthly_revenue is not None:
        update_doc["monthly_revenue"] = updates.monthly_revenue
    
    # Update user in database
    await db.users.update_one(
        {"_id": current_user.id},
        {"$set": update_doc}
    )
    
    # Get updated user
    updated_user = await db.users.find_one({"_id": current_user.id})
    
    return {
        "user": {
            "id": str(updated_user["_id"]),
            "email": updated_user["email"],
            "first_name": updated_user["first_name"],
            "last_name": updated_user["last_name"],
            "business_name": updated_user["business_name"],
            "phone": updated_user.get("phone"),
            "industry": updated_user.get("industry"),
            "employees": updated_user.get("employees"),
            "monthly_revenue": updated_user.get("monthly_revenue")
        }
    }


@router.delete("/account", response_model=dict)
async def delete_account(current_user: UserInDB = Depends(get_current_user)):
    """Delete user account and all related data."""
    db = get_database()
    
    # Delete user
    await db.users.delete_one({"_id": current_user.id})
    
    # Delete related data (transactions, subscriptions, etc.)
    await db.transactions.delete_many({"user_id": current_user.id})
    await db.subscriptions.delete_many({"user_id": current_user.id})
    await db.connected_accounts.delete_many({"user_id": current_user.id})
    await db.ai_conversations.delete_many({"user_id": current_user.id})
    
    return {"message": "Account deleted successfully"}
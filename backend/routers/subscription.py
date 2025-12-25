"""Subscription routes."""
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from bson import ObjectId

from models.subscription import SubscriptionInDB, SubscriptionResponse
from models.user import UserInDB
from auth.dependencies import get_current_user
from database import get_database


router = APIRouter(prefix="/api/v1/subscription", tags=["subscription"])


@router.get("/status", response_model=SubscriptionResponse)
async def get_subscription_status(current_user: UserInDB = Depends(get_current_user)):
    """Get user subscription status."""
    db = get_database()
    
    # Get subscription from database
    subscription = await db.subscriptions.find_one({"user_id": current_user.id})
    
    if not subscription:
        # No subscription found, return default free plan
        return SubscriptionResponse(
            hasAccess=False,  # Free plan has no premium access
            isTrialActive=False,
            trialEndsAt=None,
            plan="free"
        )
    
    # Check if trial has expired
    is_trial_active = subscription.get("is_trial_active", False)
    trial_ends_at = subscription.get("trial_ends_at")
    
    if is_trial_active and trial_ends_at:
        # Check if trial has expired
        if datetime.utcnow() > trial_ends_at:
            # Trial has expired, update subscription
            await db.subscriptions.update_one(
                {"_id": subscription["_id"]},
                {"$set": {
                    "is_trial_active": False,
                    "updated_at": datetime.utcnow()
                }}
            )
            is_trial_active = False
    
    # Determine access
    has_access = is_trial_active or subscription.get("plan") == "premium"
    
    return SubscriptionResponse(
        hasAccess=has_access,
        isTrialActive=is_trial_active,
        trialEndsAt=trial_ends_at.isoformat() + "Z" if trial_ends_at else None,
        plan=subscription.get("plan", "free")
    )


@router.post("/start-trial", response_model=dict)
async def start_trial(current_user: UserInDB = Depends(get_current_user)):
    """Start 14-day free trial."""
    db = get_database()
    
    # Get existing subscription
    subscription = await db.subscriptions.find_one({"user_id": current_user.id})
    
    if subscription:
        # Check if trial was already used
        if subscription.get("trial_started_at"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Trial has already been used"
            )
        
        # Update existing subscription to start trial
        trial_started_at = datetime.utcnow()
        trial_ends_at = trial_started_at + timedelta(days=14)
        
        await db.subscriptions.update_one(
            {"_id": subscription["_id"]},
            {"$set": {
                "is_trial_active": True,
                "trial_started_at": trial_started_at,
                "trial_ends_at": trial_ends_at,
                "updated_at": datetime.utcnow()
            }}
        )
    else:
        # Create new subscription with trial
        trial_started_at = datetime.utcnow()
        trial_ends_at = trial_started_at + timedelta(days=14)
        
        subscription_doc = {
            "user_id": current_user.id,
            "is_trial_active": True,
            "trial_started_at": trial_started_at,
            "trial_ends_at": trial_ends_at,
            "plan": "free",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        await db.subscriptions.insert_one(subscription_doc)
    
    return {
        "message": "Trial started successfully",
        "trialEndsAt": trial_ends_at.isoformat() + "Z"
    }
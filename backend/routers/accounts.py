"""Account connection routes."""
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from bson import ObjectId
from typing import List

from models.connected_account import ConnectedAccountCreate, ConnectedAccountResponse
from models.user import UserInDB
from auth.dependencies import get_current_user
from database import get_database
from services.sample_data_seeder import seed_sample_data_for_user


router = APIRouter(prefix="/api/v1/accounts", tags=["accounts"])


@router.post("/connect", response_model=dict, status_code=status.HTTP_201_CREATED)
async def connect_account(
    account_data: ConnectedAccountCreate,
    current_user: UserInDB = Depends(get_current_user)
):
    """
    Simulate connecting a financial account (Square, Stripe, or Bank).
    
    Creates a connected account record for the user.
    """
    db = get_database()
    
    # Validate source
    valid_sources = ["square", "stripe", "bank"]
    if account_data.source.lower() not in valid_sources:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid source. Must be one of: {', '.join(valid_sources)}"
        )
    
    # Check if account already exists
    existing_account = await db.connected_accounts.find_one({
        "user_id": current_user.id,
        "source": account_data.source.lower(),
        "name": account_data.name
    })
    
    if existing_account:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This account is already connected"
        )
    
    # Check if this is the user's FIRST account connection
    account_count = await db.connected_accounts.count_documents({"user_id": current_user.id})
    is_first_account = (account_count == 0)
    
    # Create connected account document
    account_doc = {
        "user_id": current_user.id,
        "source": account_data.source.lower(),
        "name": account_data.name,
        "connected_at": datetime.utcnow()
    }
    
    # Insert into database
    result = await db.connected_accounts.insert_one(account_doc)
    account_id = str(result.inserted_id)
    
    # If this is the first account, automatically seed sample data
    if is_first_account:
        try:
            print(f"[AUTO-SEED] First account connected for user {current_user.id}, seeding sample data...")
            await seed_sample_data_for_user(db, current_user.id)
            print(f"[AUTO-SEED] Sample data seeded successfully for user {current_user.id}")
        except Exception as e:
            # Don't fail the account connection if seeding fails
            print(f"[AUTO-SEED] Warning: Failed to seed sample data: {e}")
    
    return {
        "account": {
            "id": account_id,
            "source": account_data.source.lower(),
            "name": account_data.name,
            "connected_at": account_doc["connected_at"].isoformat() + "Z"
        },
        "sample_data_seeded": is_first_account
    }


@router.get("/connected", response_model=dict)
async def get_connected_accounts(current_user: UserInDB = Depends(get_current_user)):
    """
    Get all connected accounts for the current user.
    
    Returns a list of all accounts the user has connected.
    """
    db = get_database()
    
    # Fetch all connected accounts for user
    accounts_cursor = db.connected_accounts.find({"user_id": current_user.id})
    accounts = await accounts_cursor.to_list(length=None)
    
    # Convert to response format
    account_list = []
    for acc in accounts:
        account_list.append({
            "id": str(acc["_id"]),
            "source": acc["source"],
            "name": acc["name"],
            "connected_at": acc["connected_at"].isoformat() + "Z"
        })
    
    return {"accounts": account_list}


@router.delete("/{account_id}", response_model=dict)
async def disconnect_account(
    account_id: str,
    current_user: UserInDB = Depends(get_current_user)
):
    """
    Disconnect a connected account.
    
    Removes the account connection and optionally deletes associated transactions.
    """
    db = get_database()
    
    # Validate account_id
    if not ObjectId.is_valid(account_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid account ID"
        )
    
    # Find account
    account = await db.connected_accounts.find_one({
        "_id": ObjectId(account_id),
        "user_id": current_user.id
    })
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    
    # Delete account
    await db.connected_accounts.delete_one({"_id": ObjectId(account_id)})
    
    return {"message": "Account disconnected successfully"}
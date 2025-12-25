"""Transaction routes."""
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from bson import ObjectId
from pydantic import BaseModel

from models.user import UserInDB
from auth.dependencies import get_current_user
from database import get_database
from services.transaction_generator import generate_transactions_for_source


router = APIRouter(prefix="/api/v1/transactions", tags=["transactions"])


class SyncRequest(BaseModel):
    """Transaction sync request schema."""
    source: str


@router.post("/sync", response_model=dict)
async def sync_transactions(
    sync_data: SyncRequest,
    current_user: UserInDB = Depends(get_current_user)
):
    """
    Simulate syncing transactions from a connected account.
    
    Generates mock transaction data based on the account source (Square, Stripe, or Bank).
    """
    db = get_database()
    
    # Validate source
    valid_sources = ["square", "stripe", "bank"]
    source = sync_data.source.lower()
    
    if source not in valid_sources:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid source. Must be one of: {', '.join(valid_sources)}"
        )
    
    # Check if user has this account connected
    connected_account = await db.connected_accounts.find_one({
        "user_id": current_user.id,
        "source": source
    })
    
    if not connected_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No {source} account connected. Please connect the account first."
        )
    
    # Generate mock transactions
    mock_transactions = generate_transactions_for_source(source)
    
    # Insert transactions into database
    transactions_to_insert = []
    for trans in mock_transactions:
        transaction_doc = {
            "user_id": current_user.id,
            "date": trans["date"],
            "vendor": trans["vendor"],
            "amount": trans["amount"],
            "category": trans["category"],
            "confidence": trans["confidence"],
            "status": trans["status"],
            "explanation": trans["explanation"],
            "payment_method": trans["payment_method"],
            "original_description": trans.get("original_description"),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        transactions_to_insert.append(transaction_doc)
    
    # Insert all transactions
    if transactions_to_insert:
        result = await db.transactions.insert_many(transactions_to_insert)
        count = len(result.inserted_ids)
    else:
        count = 0
    
    return {
        "message": "Sync completed successfully",
        "count": count,
        "source": source
    }


@router.get("", response_model=dict)
async def get_transactions(
    status: str = None,
    search: str = None,
    current_user: UserInDB = Depends(get_current_user)
):
    """
    Get all transactions for the current user with optional filtering.
    
    Query parameters:
    - status: Filter by status (all, auto-approved, needs-review, manual)
    - search: Search by vendor or category name
    """
    db = get_database()
    
    # Build query
    query = {"user_id": current_user.id}
    
    # Add status filter
    if status and status != "all":
        query["status"] = status
    
    # Add search filter
    if search:
        query["$or"] = [
            {"vendor": {"$regex": search, "$options": "i"}},
            {"category": {"$regex": search, "$options": "i"}}
        ]
    
    # Fetch transactions
    transactions_cursor = db.transactions.find(query).sort("date", -1)
    transactions = await transactions_cursor.to_list(length=None)
    
    # Convert to response format
    transaction_list = []
    for trans in transactions:
        transaction_list.append({
            "id": str(trans["_id"]),
            "date": trans["date"].isoformat() + "Z",
            "vendor": trans["vendor"],
            "amount": trans["amount"],
            "category": trans["category"],
            "confidence": trans["confidence"],
            "status": trans["status"],
            "explanation": trans["explanation"],
            "payment_method": trans["payment_method"],
            "original_description": trans.get("original_description")
        })
    
    return {"transactions": transaction_list}


@router.get("/{transaction_id}", response_model=dict)
async def get_transaction(
    transaction_id: str,
    current_user: UserInDB = Depends(get_current_user)
):
    """Get a single transaction by ID."""
    db = get_database()
    
    # Validate transaction_id
    if not ObjectId.is_valid(transaction_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid transaction ID"
        )
    
    # Find transaction
    transaction = await db.transactions.find_one({
        "_id": ObjectId(transaction_id),
        "user_id": current_user.id
    })
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    return {
        "id": str(transaction["_id"]),
        "date": transaction["date"].isoformat() + "Z",
        "vendor": transaction["vendor"],
        "amount": transaction["amount"],
        "category": transaction["category"],
        "confidence": transaction["confidence"],
        "status": transaction["status"],
        "explanation": transaction["explanation"],
        "payment_method": transaction["payment_method"],
        "original_description": transaction.get("original_description")
    }


class UpdateTransactionRequest(BaseModel):
    """Transaction update request schema."""
    category: str = None
    status: str = None


@router.put("/{transaction_id}", response_model=dict)
async def update_transaction(
    transaction_id: str,
    update_data: UpdateTransactionRequest,
    current_user: UserInDB = Depends(get_current_user)
):
    """Update a transaction's category or status."""
    category = update_data.category
    status = update_data.status
    db = get_database()
    
    # Validate transaction_id
    if not ObjectId.is_valid(transaction_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid transaction ID"
        )
    
    # Find transaction
    transaction = await db.transactions.find_one({
        "_id": ObjectId(transaction_id),
        "user_id": current_user.id
    })
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    # Build update document
    update_doc = {"updated_at": datetime.utcnow()}
    
    if category is not None:
        update_doc["category"] = category
    
    if status is not None:
        valid_statuses = ["auto-approved", "needs-review", "manual"]
        if status not in valid_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            )
        update_doc["status"] = status
    
    # Update transaction
    await db.transactions.update_one(
        {"_id": ObjectId(transaction_id)},
        {"$set": update_doc}
    )
    
    # Get updated transaction
    updated_transaction = await db.transactions.find_one({"_id": ObjectId(transaction_id)})
    
    return {
        "transaction": {
            "id": str(updated_transaction["_id"]),
            "date": updated_transaction["date"].isoformat() + "Z",
            "vendor": updated_transaction["vendor"],
            "amount": updated_transaction["amount"],
            "category": updated_transaction["category"],
            "confidence": updated_transaction["confidence"],
            "status": updated_transaction["status"],
            "explanation": updated_transaction["explanation"],
            "payment_method": updated_transaction["payment_method"],
            "original_description": updated_transaction.get("original_description")
        }
    }
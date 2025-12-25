"""
Mock Plaid service for development without real API credentials.
This allows testing the bank connection flow with sample data.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
import uuid

from auth.dependencies import get_current_user
from models.user import UserInDB
from database import get_database


router = APIRouter(prefix="/api/plaid", tags=["plaid"])


class LinkTokenResponse(BaseModel):
    link_token: str
    expiration: str


class ExchangeTokenRequest(BaseModel):
    public_token: str


class ExchangeTokenResponse(BaseModel):
    access_token: str
    item_id: str


class TransactionData(BaseModel):
    transaction_id: str
    date: str
    name: str
    amount: float
    category: Optional[list[str]] = None
    merchant_name: Optional[str] = None
    payment_channel: str


# Sample transaction data for development
SAMPLE_TRANSACTIONS = [
    {
        "name": "Starbucks Coffee",
        "amount": 5.75,
        "category": ["Food and Drink", "Restaurants", "Coffee Shop"],
        "merchant_name": "Starbucks",
        "payment_channel": "in store"
    },
    {
        "name": "Amazon.com",
        "amount": 89.99,
        "category": ["Shops", "Online Marketplaces"],
        "merchant_name": "Amazon",
        "payment_channel": "online"
    },
    {
        "name": "Shell Gas Station",
        "amount": 45.20,
        "category": ["Transportation", "Gas Stations"],
        "merchant_name": "Shell",
        "payment_channel": "in store"
    },
    {
        "name": "Whole Foods Market",
        "amount": 127.43,
        "category": ["Food and Drink", "Groceries"],
        "merchant_name": "Whole Foods",
        "payment_channel": "in store"
    },
    {
        "name": "Netflix Subscription",
        "amount": 15.99,
        "category": ["Service", "Subscription"],
        "merchant_name": "Netflix",
        "payment_channel": "online"
    },
    {
        "name": "Office Depot",
        "amount": 234.56,
        "category": ["Shops", "Office Supplies"],
        "merchant_name": "Office Depot",
        "payment_channel": "in store"
    },
    {
        "name": "Electric Company Payment",
        "amount": 156.78,
        "category": ["Service", "Utilities", "Electric"],
        "merchant_name": "Electric Co",
        "payment_channel": "online"
    },
    {
        "name": "Target",
        "amount": 78.90,
        "category": ["Shops", "Department Stores"],
        "merchant_name": "Target",
        "payment_channel": "in store"
    },
    {
        "name": "Uber Ride",
        "amount": 23.45,
        "category": ["Transportation", "Taxi"],
        "merchant_name": "Uber",
        "payment_channel": "online"
    },
    {
        "name": "AT&T Wireless",
        "amount": 85.00,
        "category": ["Service", "Telecommunications"],
        "merchant_name": "AT&T",
        "payment_channel": "online"
    }
]


@router.post("/create_link_token", response_model=LinkTokenResponse)
async def create_link_token(current_user: UserInDB = Depends(get_current_user)):
    """
    Create a mock Plaid Link token for development.
    Returns a fake token that can be used to simulate the bank connection flow.
    """
    # Generate a mock link token
    mock_token = f"link-sandbox-{uuid.uuid4()}"
    expiration = (datetime.utcnow() + timedelta(hours=4)).isoformat() + "Z"
    
    return LinkTokenResponse(
        link_token=mock_token,
        expiration=expiration
    )


@router.post("/exchange_public_token", response_model=ExchangeTokenResponse)
async def exchange_public_token(
    request: ExchangeTokenRequest,
    current_user: UserInDB = Depends(get_current_user)
):
    """
    Exchange a mock public token for a mock access token.
    Simulates the Plaid token exchange process with sample data.
    """
    # Generate mock tokens
    mock_access_token = f"access-sandbox-{uuid.uuid4()}"
    mock_item_id = f"item-sandbox-{uuid.uuid4()}"
    
    # Store mock access token in database
    db = get_database()
    await db.users.update_one(
        {"_id": current_user.id},
        {
            "$set": {
                "plaid_access_token": mock_access_token,
                "plaid_item_id": mock_item_id,
                "bank_connected_at": datetime.utcnow(),
                "is_mock_plaid": True  # Flag to indicate this is mock data
            }
        }
    )
    
    return ExchangeTokenResponse(
        access_token=mock_access_token,
        item_id=mock_item_id
    )


@router.get("/transactions")
async def get_transactions(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    current_user: UserInDB = Depends(get_current_user)
):
    """
    Return sample transaction data for development.
    Generates realistic-looking transactions for the specified date range.
    """
    # Get user's access token from database
    db = get_database()
    user_data = await db.users.find_one({"_id": current_user.id})
    
    if not user_data or "plaid_access_token" not in user_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No bank account connected. Please connect a bank account first."
        )
    
    # Default to last 90 days if no dates provided
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")
    if not start_date:
        start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
    
    # Generate sample transactions with dates in the range
    formatted_transactions = []
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    days_range = (end_dt - start_dt).days
    
    # Create transactions spread across the date range
    for i, sample_txn in enumerate(SAMPLE_TRANSACTIONS):
        # Distribute transactions across the date range
        days_offset = (i * days_range) // len(SAMPLE_TRANSACTIONS)
        txn_date = start_dt + timedelta(days=days_offset)
        
        formatted_transactions.append(TransactionData(
            transaction_id=f"txn-mock-{uuid.uuid4()}",
            date=txn_date.strftime("%Y-%m-%d"),
            name=sample_txn["name"],
            amount=sample_txn["amount"],
            category=sample_txn["category"],
            merchant_name=sample_txn["merchant_name"],
            payment_channel=sample_txn["payment_channel"]
        ))
    
    return {
        "transactions": formatted_transactions,
        "total_count": len(formatted_transactions),
        "start_date": start_date,
        "end_date": end_date,
        "is_mock_data": True  # Indicate this is sample data
    }


@router.post("/webhook")
async def plaid_webhook(webhook_data: dict):
    """
    Mock webhook endpoint for development.
    """
    return {"status": "received", "is_mock": True}
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional
import plaid
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from datetime import datetime, timedelta

from config import settings
from auth.dependencies import get_current_user
from models.user import UserInDB
from database import get_database


router = APIRouter(prefix="/api/plaid", tags=["plaid"])


# Initialize Plaid client
configuration = plaid.Configuration(
    host=plaid.Environment.Sandbox if settings.plaid_env == "sandbox" 
         else plaid.Environment.Development if settings.plaid_env == "development"
         else plaid.Environment.Production,
    api_key={
        'clientId': settings.plaid_client_id,
        'secret': settings.plaid_secret,
    }
)

api_client = plaid.ApiClient(configuration)
plaid_client = plaid_api.PlaidApi(api_client)


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


@router.post("/create_link_token", response_model=LinkTokenResponse)
async def create_link_token(current_user: UserInDB = Depends(get_current_user)):
    """
    Create a Plaid Link token for the user to connect their bank account.
    This token is used to initialize the Plaid Link UI.
    """
    try:
        request = LinkTokenCreateRequest(
            user=LinkTokenCreateRequestUser(
                client_user_id=str(current_user.id)
            ),
            client_name="FinSense",
            products=[Products("transactions")],
            country_codes=[CountryCode("US")],
            language="en",
            webhook="https://your-domain.com/api/plaid/webhook",  # Update with actual webhook URL
            # Skip phone verification in sandbox for easier testing
            # user_phone_number_verification_enabled=False  # Uncomment if needed
        )
        
        response = plaid_client.link_token_create(request)
        
        # Access response as object attributes, not dictionary
        link_token = response.link_token
        expiration = response.expiration
        
        # Convert expiration to string if it's a datetime object
        if hasattr(expiration, 'isoformat'):
            expiration = expiration.isoformat()
        else:
            expiration = str(expiration)
        
        return LinkTokenResponse(
            link_token=link_token,
            expiration=expiration
        )
    except plaid.ApiException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create link token: {e}"
        )


@router.post("/exchange_public_token", response_model=ExchangeTokenResponse)
async def exchange_public_token(
    request: ExchangeTokenRequest,
    current_user: UserInDB = Depends(get_current_user)
):
    """
    Exchange a public token for an access token after user successfully links their bank.
    The access token is stored securely and used for future API calls.
    """
    try:
        print(f"Received public_token: {request.public_token}")
        
        exchange_request = ItemPublicTokenExchangeRequest(
            public_token=request.public_token
        )
        
        print("Calling Plaid API to exchange token...")
        exchange_response = plaid_client.item_public_token_exchange(exchange_request)
        print(f"Exchange response type: {type(exchange_response)}")
        print(f"Exchange response: {exchange_response}")
        
        # Try to access response - it might be a dict-like object
        try:
            access_token = exchange_response.access_token
            item_id = exchange_response.item_id
            print(f"Accessed as attributes - access_token: {access_token}, item_id: {item_id}")
        except AttributeError:
            # Try dictionary access
            access_token = exchange_response['access_token']
            item_id = exchange_response['item_id']
            print(f"Accessed as dict - access_token: {access_token}, item_id: {item_id}")
        
        # Store access token in database associated with user
        db = get_database()
        await db.users.update_one(
            {"_id": current_user.id},
            {
                "$set": {
                    "plaid_access_token": access_token,
                    "plaid_item_id": item_id,
                    "bank_connected_at": datetime.utcnow()
                }
            }
        )
        
        return ExchangeTokenResponse(
            access_token=access_token,
            item_id=item_id
        )
    except plaid.ApiException as e:
        print(f"Plaid API Exception: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to exchange public token: {e}"
        )
    except Exception as e:
        print(f"General Exception in exchange_public_token: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to exchange public token: {str(e)}"
        )


@router.get("/transactions")
async def get_transactions(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    current_user: UserInDB = Depends(get_current_user)
):
    """
    Fetch transactions from Plaid for the connected bank account.
    Returns structured transaction data for the specified date range.
    """
    try:
        # Get user's access token from database
        db = get_database()
        user_data = await db.users.find_one({"_id": current_user.id})
        
        if not user_data or "plaid_access_token" not in user_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No bank account connected. Please connect a bank account first."
            )
        
        access_token = user_data["plaid_access_token"]
        
        # Default to last 90 days if no dates provided
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
        if not start_date:
            start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
        
        # Fetch transactions from Plaid
        request = TransactionsGetRequest(
            access_token=access_token,
            start_date=datetime.strptime(start_date, "%Y-%m-%d").date(),
            end_date=datetime.strptime(end_date, "%Y-%m-%d").date(),
            options=TransactionsGetRequestOptions(
                count=500,
                offset=0
            )
        )
        
        response = plaid_client.transactions_get(request)
        
        # Access response as object attributes
        transactions = response.transactions
        
        # Transform transactions to our format
        formatted_transactions = []
        for txn in transactions:
            formatted_transactions.append(TransactionData(
                transaction_id=txn.transaction_id,
                date=str(txn.date),
                name=txn.name,
                amount=float(txn.amount),
                category=getattr(txn, 'category', None),
                merchant_name=getattr(txn, 'merchant_name', None),
                payment_channel=txn.payment_channel
            ))
        
        return {
            "transactions": formatted_transactions,
            "total_count": len(formatted_transactions),
            "start_date": start_date,
            "end_date": end_date
        }
        
    except plaid.ApiException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch transactions: {e}"
        )


@router.post("/webhook")
async def plaid_webhook(webhook_data: dict):
    """
    Handle webhooks from Plaid for transaction updates and other events.
    """
    # Implement webhook handling logic based on your needs
    webhook_type = webhook_data.get("webhook_type")
    webhook_code = webhook_data.get("webhook_code")
    
    # Log webhook for debugging
    print(f"Received Plaid webhook: {webhook_type} - {webhook_code}")
    
    # Handle different webhook types
    if webhook_type == "TRANSACTIONS":
        if webhook_code == "INITIAL_UPDATE":
            # Initial transaction data is ready
            pass
        elif webhook_code == "HISTORICAL_UPDATE":
            # Historical transaction data is ready
            pass
        elif webhook_code == "DEFAULT_UPDATE":
            # New transaction data available
            pass
    
    return {"status": "received"}
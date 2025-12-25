from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Optional, List
import stripe
from datetime import datetime, timedelta
from urllib.parse import urlencode

from config import settings
from auth.dependencies import get_current_user
from models.user import UserInDB
from database import get_database


router = APIRouter(prefix="/api/stripe", tags=["stripe"])

# Initialize Stripe
stripe.api_key = settings.stripe_secret_key


class StripeAuthResponse(BaseModel):
    authorization_url: str


class StripeAccountInfo(BaseModel):
    stripe_user_id: str
    account_name: str
    email: Optional[str] = None


class StripeCharge(BaseModel):
    charge_id: str
    amount: float
    currency: str
    status: str
    created: str
    description: Optional[str] = None
    customer_email: Optional[str] = None
    payment_method_type: str


class StripePaymentIntent(BaseModel):
    payment_intent_id: str
    amount: float
    currency: str
    status: str
    created: str
    description: Optional[str] = None
    customer_email: Optional[str] = None


@router.get("/authorize", response_model=StripeAuthResponse)
async def stripe_authorize(current_user: UserInDB = Depends(get_current_user)):
    """
    Generate Stripe OAuth authorization URL for connecting a Stripe account.
    User will be redirected to Stripe to authorize the connection.
    In mock mode, returns a special URL that the frontend can detect.
    """
    try:
        # Check if we're in mock mode (placeholder credentials)
        is_mock_mode = (
            not settings.stripe_client_id or
            settings.stripe_client_id == "ca_your-stripe-client-id" or
            settings.stripe_client_id.startswith("ca_your-")
        )
        
        if is_mock_mode:
            # Return a mock authorization URL that frontend can detect
            frontend_url = settings.cors_origins.split(",")[0]
            return StripeAuthResponse(
                authorization_url=f"{frontend_url}/connect-accounts?stripe=mock&user_id={current_user.id}"
            )
        
        # Build real OAuth authorization URL
        params = {
            'client_id': settings.stripe_client_id,
            'state': str(current_user.id),  # Use user ID as state for verification
            'scope': 'read_only',  # Request read-only access
            'response_type': 'code',
            'redirect_uri': f'{settings.cors_origins.split(",")[0]}/stripe/callback',
        }
        
        authorization_url = f'https://connect.stripe.com/oauth/authorize?{urlencode(params)}'
        
        return StripeAuthResponse(authorization_url=authorization_url)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate authorization URL: {str(e)}"
        )


@router.get("/callback")
async def stripe_callback(code: str, state: str):
    """
    Handle OAuth callback from Stripe after user authorizes the connection.
    Exchange authorization code for access token and store it.
    """
    try:
        # Exchange authorization code for access token
        response = stripe.OAuth.token(
            grant_type='authorization_code',
            code=code,
        )
        
        stripe_user_id = response['stripe_user_id']
        access_token = response['access_token']
        
        # Store access token in database
        db = get_database()
        user_id = state  # State contains user ID
        
        await db.users.update_one(
            {"_id": user_id},
            {
                "$set": {
                    "stripe_access_token": access_token,
                    "stripe_user_id": stripe_user_id,
                    "stripe_connected_at": datetime.utcnow()
                }
            }
        )
        
        # Redirect back to frontend with success
        frontend_url = settings.cors_origins.split(",")[0]
        return RedirectResponse(url=f"{frontend_url}/connect-accounts?stripe=success")
        
    except stripe.oauth_error.OAuthError as e:
        # Redirect back to frontend with error
        frontend_url = settings.cors_origins.split(",")[0]
        return RedirectResponse(url=f"{frontend_url}/connect-accounts?stripe=error&message={str(e)}")
    except Exception as e:
        frontend_url = settings.cors_origins.split(",")[0]
        return RedirectResponse(url=f"{frontend_url}/connect-accounts?stripe=error&message={str(e)}")


@router.get("/account")
async def get_stripe_account(current_user: UserInDB = Depends(get_current_user)):
    """
    Get information about the connected Stripe account.
    """
    try:
        db = get_database()
        user_data = await db.users.find_one({"_id": current_user.id})
        
        if not user_data or "stripe_access_token" not in user_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No Stripe account connected"
            )
        
        # Get account info using the connected account's access token
        account = stripe.Account.retrieve(
            stripe_account=user_data["stripe_user_id"]
        )
        
        return StripeAccountInfo(
            stripe_user_id=account.id,
            account_name=account.business_profile.name if account.business_profile else "Stripe Account",
            email=account.email
        )
        
    except stripe.error.StripeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Stripe API error: {str(e)}"
        )


@router.get("/charges")
async def get_stripe_charges(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = 100,
    current_user: UserInDB = Depends(get_current_user)
):
    """
    Fetch charges (payments) from the connected Stripe account.
    Returns payment transaction data for the specified date range.
    """
    try:
        db = get_database()
        user_data = await db.users.find_one({"_id": current_user.id})
        
        if not user_data or "stripe_access_token" not in user_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No Stripe account connected"
            )
        
        # Build query parameters
        params = {
            'limit': min(limit, 100),  # Max 100 per request
        }
        
        # Add date filters if provided
        if start_date:
            start_timestamp = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())
            params['created'] = {'gte': start_timestamp}
        
        if end_date:
            end_timestamp = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp())
            if 'created' in params:
                params['created']['lte'] = end_timestamp
            else:
                params['created'] = {'lte': end_timestamp}
        
        # Fetch charges from Stripe
        charges = stripe.Charge.list(
            **params,
            stripe_account=user_data["stripe_user_id"]
        )
        
        # Transform charges to our format
        formatted_charges = []
        for charge in charges.data:
            formatted_charges.append(StripeCharge(
                charge_id=charge.id,
                amount=charge.amount / 100,  # Convert from cents to dollars
                currency=charge.currency.upper(),
                status=charge.status,
                created=datetime.fromtimestamp(charge.created).strftime("%Y-%m-%d %H:%M:%S"),
                description=charge.description,
                customer_email=charge.billing_details.email if charge.billing_details else None,
                payment_method_type=charge.payment_method_details.type if charge.payment_method_details else "unknown"
            ))
        
        return {
            "charges": formatted_charges,
            "total_count": len(formatted_charges),
            "has_more": charges.has_more
        }
        
    except stripe.error.StripeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Stripe API error: {str(e)}"
        )


@router.get("/payment-intents")
async def get_stripe_payment_intents(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = 100,
    current_user: UserInDB = Depends(get_current_user)
):
    """
    Fetch payment intents from the connected Stripe account.
    Payment intents represent the full payment lifecycle.
    """
    try:
        db = get_database()
        user_data = await db.users.find_one({"_id": current_user.id})
        
        if not user_data or "stripe_access_token" not in user_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No Stripe account connected"
            )
        
        # Build query parameters
        params = {
            'limit': min(limit, 100),
        }
        
        # Add date filters if provided
        if start_date:
            start_timestamp = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())
            params['created'] = {'gte': start_timestamp}
        
        if end_date:
            end_timestamp = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp())
            if 'created' in params:
                params['created']['lte'] = end_timestamp
            else:
                params['created'] = {'lte': end_timestamp}
        
        # Fetch payment intents from Stripe
        payment_intents = stripe.PaymentIntent.list(
            **params,
            stripe_account=user_data["stripe_user_id"]
        )
        
        # Transform payment intents to our format
        formatted_intents = []
        for intent in payment_intents.data:
            formatted_intents.append(StripePaymentIntent(
                payment_intent_id=intent.id,
                amount=intent.amount / 100,  # Convert from cents to dollars
                currency=intent.currency.upper(),
                status=intent.status,
                created=datetime.fromtimestamp(intent.created).strftime("%Y-%m-%d %H:%M:%S"),
                description=intent.description,
                customer_email=intent.receipt_email
            ))
        
        return {
            "payment_intents": formatted_intents,
            "total_count": len(formatted_intents),
            "has_more": payment_intents.has_more
        }
        
    except stripe.error.StripeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Stripe API error: {str(e)}"
        )


@router.post("/webhook")
async def stripe_webhook(request: Request):
    """
    Handle webhooks from Stripe for payment events.
    Verifies webhook signature and processes events.
    """
    try:
        payload = await request.body()
        sig_header = request.headers.get('stripe-signature')
        
        if not settings.stripe_webhook_secret:
            # If no webhook secret configured, just log the event
            event = stripe.Event.construct_from(
                await request.json(), stripe.api_key
            )
        else:
            # Verify webhook signature
            try:
                event = stripe.Webhook.construct_event(
                    payload, sig_header, settings.stripe_webhook_secret
                )
            except stripe.error.SignatureVerificationError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid signature"
                )
        
        # Handle different event types
        event_type = event['type']
        
        if event_type == 'charge.succeeded':
            # Handle successful charge
            charge = event['data']['object']
            print(f"Charge succeeded: {charge['id']}")
            
        elif event_type == 'payment_intent.succeeded':
            # Handle successful payment intent
            payment_intent = event['data']['object']
            print(f"Payment intent succeeded: {payment_intent['id']}")
            
        elif event_type == 'charge.refunded':
            # Handle refund
            charge = event['data']['object']
            print(f"Charge refunded: {charge['id']}")
        
        # Add more event handlers as needed
        
        return {"status": "success"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Webhook processing error: {str(e)}"
        )


@router.delete("/disconnect")
async def disconnect_stripe(current_user: UserInDB = Depends(get_current_user)):
    """
    Disconnect the Stripe account by removing stored credentials.
    """
    try:
        db = get_database()
        
        await db.users.update_one(
            {"_id": current_user.id},
            {
                "$unset": {
                    "stripe_access_token": "",
                    "stripe_user_id": "",
                    "stripe_connected_at": ""
                }
            }
        )
        
        return {"message": "Stripe account disconnected successfully"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to disconnect Stripe account: {str(e)}"
        )
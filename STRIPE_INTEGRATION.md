# Stripe Payment Processing Integration

This document describes the Stripe integration implemented for connecting Stripe accounts to sync payment processing data in FinSense AI.

## Overview

The integration follows the Stripe Connect OAuth flow:
1. Customer clicks "Connect Account" for Stripe
2. Frontend requests authorization URL from backend
3. User is redirected to Stripe OAuth page
4. User authorizes the connection with their Stripe account
5. Stripe redirects back with authorization code
6. Backend exchanges code for access token
7. Backend stores access token and fetches payment data
8. Stripe returns structured payment transaction data

## Backend Implementation

### 1. Dependencies (`backend/requirements.txt`)
```
stripe>=7.0.0
```

### 2. Configuration (`backend/config.py`)
Added Stripe configuration settings:
- `stripe_secret_key`: Your Stripe secret API key
- `stripe_client_id`: Your Stripe Connect client ID
- `stripe_webhook_secret`: Webhook signing secret (optional)

### 3. Environment Variables (`backend/.env.example`)
```env
STRIPE_SECRET_KEY=sk_test_your-stripe-secret-key
STRIPE_CLIENT_ID=ca_your-stripe-client-id
STRIPE_WEBHOOK_SECRET=whsec_your-webhook-secret
```

### 4. Stripe Router (`backend/routers/stripe.py`)

#### Endpoints:

**GET `/api/stripe/authorize`**
- Generates Stripe OAuth authorization URL
- Requires authentication
- Returns: `{ authorization_url }`
- User is redirected to this URL to authorize the connection

**GET `/api/stripe/callback`**
- Handles OAuth callback from Stripe
- Exchanges authorization code for access token
- Stores access token in user's database record
- Query params: `code` (authorization code), `state` (user ID)
- Redirects to frontend with success/error status

**GET `/api/stripe/account`**
- Gets information about the connected Stripe account
- Requires authentication and connected Stripe account
- Returns: `{ stripe_user_id, account_name, email }`

**GET `/api/stripe/charges`**
- Fetches charges (completed payments) from Stripe
- Query params: `start_date`, `end_date`, `limit` (optional)
- Requires authentication and connected Stripe account
- Returns: Array of charge data with amounts, status, customer info

**GET `/api/stripe/payment-intents`**
- Fetches payment intents from Stripe
- Payment intents represent the full payment lifecycle
- Query params: `start_date`, `end_date`, `limit` (optional)
- Requires authentication and connected Stripe account
- Returns: Array of payment intent data

**POST `/api/stripe/webhook`**
- Handles webhooks from Stripe for real-time payment events
- Verifies webhook signature if webhook secret is configured
- Processes events like charge.succeeded, payment_intent.succeeded, etc.

**DELETE `/api/stripe/disconnect`**
- Disconnects Stripe account by removing stored credentials
- Requires authentication
- Returns: Success message

### 5. Database Schema Updates
User documents now include:
- `stripe_access_token`: Access token for Stripe API calls
- `stripe_user_id`: Stripe connected account ID
- `stripe_connected_at`: Timestamp of Stripe connection

## Frontend Implementation

### 1. Types (`frontend/src/types/index.ts`)
```typescript
export interface StripeAuthResponse {
  authorization_url: string;
}

export interface StripeAccountInfo {
  stripe_user_id: string;
  account_name: string;
  email?: string;
}

export interface StripeCharge {
  charge_id: string;
  amount: number;
  currency: string;
  status: string;
  created: string;
  description?: string;
  customer_email?: string;
  payment_method_type: string;
}

export interface StripePaymentIntent {
  payment_intent_id: string;
  amount: number;
  currency: string;
  status: string;
  created: string;
  description?: string;
  customer_email?: string;
}
```

### 2. API Endpoints (`frontend/src/lib/api.ts`)
```typescript
stripeAuthorize: `${API_BASE_URL}/api/stripe/authorize`
stripeAccount: `${API_BASE_URL}/api/stripe/account`
stripeCharges: `${API_BASE_URL}/api/stripe/charges`
stripePaymentIntents: `${API_BASE_URL}/api/stripe/payment-intents`
stripeDisconnect: `${API_BASE_URL}/api/stripe/disconnect`
```

### 3. Connect Accounts Page (`frontend/src/pages/ConnectAccounts.tsx`)

#### Key Features:
- Fetches Stripe authorization URL when user clicks "Connect Account"
- Redirects user to Stripe OAuth page
- Handles OAuth callback with success/error status
- Shows connection status and success messages
- Allows disconnection of Stripe account

#### Flow:
1. User clicks "Connect Account" for Stripe
2. Frontend requests authorization URL from backend
3. User is redirected to Stripe OAuth page
4. User authorizes connection with their Stripe account
5. Stripe redirects back to `/connect-accounts?stripe=success`
6. Frontend detects callback and shows success message
7. User can proceed to sync progress page

## Setup Instructions

### Backend Setup:

1. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Get Stripe credentials:
   - Sign up at https://dashboard.stripe.com/register
   - Get your API keys from https://dashboard.stripe.com/apikeys
   - For Connect, register your platform at https://dashboard.stripe.com/settings/applications
   - Get your `client_id` from the Connect settings

3. Configure environment variables in `.env`:
```env
STRIPE_SECRET_KEY=sk_test_your_actual_secret_key
STRIPE_CLIENT_ID=ca_your_actual_client_id
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
```

4. Configure OAuth redirect URI in Stripe Dashboard:
   - Go to https://dashboard.stripe.com/settings/applications
   - Add redirect URI: `http://localhost:8000/api/stripe/callback` (for development)
   - For production, use your actual domain

5. Run the backend:
```bash
uvicorn main:app --reload
```

### Frontend Setup:

1. Ensure frontend is running:
```bash
cd frontend
pnpm dev
```

## Testing

### Test Mode:
Stripe provides test mode for development:
- Use test API keys (starting with `sk_test_`)
- Test mode data is separate from live mode
- No real money is processed

### Test Flow:
1. Navigate to Connect Accounts page
2. Click "Connect Account" on Stripe card
3. You'll be redirected to Stripe OAuth page
4. Authorize the connection (use your Stripe test account)
5. You'll be redirected back with success message
6. Verify connection status is shown
7. Check browser console for any errors

### Test Payment Data:
You can create test charges in your Stripe Dashboard:
1. Go to https://dashboard.stripe.com/test/payments
2. Create test payments
3. Use the API to fetch these test charges

## Security Considerations

1. **Access Token Storage**: Access tokens are stored securely in MongoDB
2. **Read-Only Scope**: OAuth requests read-only access by default
3. **State Parameter**: User ID is used as state for CSRF protection
4. **Webhook Verification**: Implement signature verification for webhooks
5. **HTTPS Required**: OAuth redirects require HTTPS in production
6. **Token Refresh**: Stripe access tokens don't expire but can be revoked

## Production Checklist

- [ ] Switch from test to live API keys
- [ ] Update OAuth redirect URI to production domain
- [ ] Configure webhook endpoint URL in Stripe Dashboard
- [ ] Implement webhook signature verification
- [ ] Add error monitoring and logging
- [ ] Test OAuth flow with real Stripe account
- [ ] Implement rate limiting for API endpoints
- [ ] Add user notification for connection issues
- [ ] Set up payment data sync scheduling
- [ ] Test disconnection and reconnection flows
- [ ] Implement proper error handling for API failures

## Payment Data Structure

### Charges
Stripe returns charges with the following structure:
```json
{
  "charge_id": "ch_xxx",
  "amount": 42.50,
  "currency": "USD",
  "status": "succeeded",
  "created": "2024-01-15 10:30:00",
  "description": "Payment for services",
  "customer_email": "customer@example.com",
  "payment_method_type": "card"
}
```

### Payment Intents
Payment intents include more detailed payment lifecycle information:
```json
{
  "payment_intent_id": "pi_xxx",
  "amount": 42.50,
  "currency": "USD",
  "status": "succeeded",
  "created": "2024-01-15 10:30:00",
  "description": "Payment for services",
  "customer_email": "customer@example.com"
}
```

## Webhook Events

Common webhook events to handle:

1. **charge.succeeded** - Payment completed successfully
2. **charge.failed** - Payment failed
3. **charge.refunded** - Payment was refunded
4. **payment_intent.succeeded** - Payment intent succeeded
5. **payment_intent.payment_failed** - Payment intent failed
6. **customer.subscription.created** - New subscription created
7. **customer.subscription.updated** - Subscription updated
8. **customer.subscription.deleted** - Subscription cancelled

## Troubleshooting

### Common Issues:

1. **Authorization URL generation fails**
   - Verify Stripe credentials in .env
   - Check client_id is correct
   - Ensure user is authenticated

2. **OAuth redirect fails**
   - Verify redirect URI matches Stripe Dashboard settings
   - Check CORS settings allow the redirect
   - Ensure callback endpoint is accessible

3. **Token exchange fails**
   - Verify authorization code is valid
   - Check Stripe API keys are correct
   - Review backend logs for Stripe API errors

4. **No payment data returned**
   - Verify access token is stored correctly
   - Check date range parameters
   - Ensure Stripe account has payment data in the period
   - Verify API permissions (read-only scope)

5. **Webhook signature verification fails**
   - Verify webhook secret is correct
   - Check webhook endpoint is publicly accessible
   - Ensure raw request body is used for verification

## Data Mapping

Map Stripe payment data to your internal transaction format:

```python
# Example mapping
transaction = {
    "id": charge.id,
    "date": datetime.fromtimestamp(charge.created),
    "vendor": charge.billing_details.name or "Stripe Payment",
    "amount": charge.amount / 100,  # Convert cents to dollars
    "category": "Revenue",
    "payment_method": charge.payment_method_details.type,
    "status": charge.status,
    "source": "stripe"
}
```

## API Rate Limits

Stripe has rate limits:
- Test mode: 100 requests per second
- Live mode: 100 requests per second
- Implement exponential backoff for rate limit errors
- Use pagination for large data sets

## Next Steps

1. Implement automatic payment data syncing via webhooks
2. Add support for Stripe subscriptions tracking
3. Implement refund handling and reconciliation
4. Add customer data synchronization
5. Create payment analytics and reporting
6. Implement dispute and chargeback tracking
7. Add support for multiple Stripe accounts per user
8. Create payment reconciliation features
9. Implement revenue recognition logic
10. Add support for Stripe Connect platforms

## Additional Resources

- [Stripe API Documentation](https://stripe.com/docs/api)
- [Stripe Connect Documentation](https://stripe.com/docs/connect)
- [Stripe OAuth Documentation](https://stripe.com/docs/connect/oauth-reference)
- [Stripe Webhooks Guide](https://stripe.com/docs/webhooks)
- [Stripe Testing Guide](https://stripe.com/docs/testing)
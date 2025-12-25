# Plaid Bank Account Integration

This document describes the Plaid integration implemented for connecting bank accounts in FinSense AI.

## Overview

The integration follows the standard Plaid Link flow:
1. Customer clicks "Connect Account" for Bank Account
2. Frontend requests a link token from backend
3. Plaid Link UI opens for user authentication
4. User authenticates with their bank through Plaid's secure UI
5. Plaid returns a public token to the frontend
6. Frontend exchanges public token for access token via backend
7. Backend stores access token and fetches transaction data
8. Plaid returns structured transaction data

## Backend Implementation

### 1. Dependencies (`backend/requirements.txt`)
```
plaid-python>=20.0.0
```

### 2. Configuration (`backend/config.py`)
Added Plaid configuration settings:
- `plaid_client_id`: Your Plaid client ID
- `plaid_secret`: Your Plaid secret key
- `plaid_env`: Environment (sandbox/development/production)

### 3. Environment Variables (`backend/.env.example`)
```env
PLAID_CLIENT_ID=your-plaid-client-id
PLAID_SECRET=your-plaid-secret-key
PLAID_ENV=sandbox
```

### 4. Plaid Router (`backend/routers/plaid.py`)

#### Endpoints:

**POST `/api/plaid/create_link_token`**
- Creates a Plaid Link token for initializing the Plaid Link UI
- Requires authentication
- Returns: `{ link_token, expiration }`

**POST `/api/plaid/exchange_public_token`**
- Exchanges public token for access token after successful bank connection
- Stores access token in user's database record
- Requires authentication
- Body: `{ public_token }`
- Returns: `{ access_token, item_id }`

**GET `/api/plaid/transactions`**
- Fetches transactions from connected bank account
- Query params: `start_date`, `end_date` (optional, defaults to last 90 days)
- Requires authentication and connected bank account
- Returns: Array of structured transaction data

**POST `/api/plaid/webhook`**
- Handles webhooks from Plaid for transaction updates
- Processes events like INITIAL_UPDATE, HISTORICAL_UPDATE, DEFAULT_UPDATE

### 5. Database Schema Updates
User documents now include:
- `plaid_access_token`: Encrypted access token for Plaid API calls
- `plaid_item_id`: Plaid item identifier
- `bank_connected_at`: Timestamp of bank connection

## Frontend Implementation

### 1. Dependencies (`frontend/package.json`)
```json
"react-plaid-link": "^3.5.2"
```

### 2. Types (`frontend/src/types/index.ts`)
```typescript
export interface PlaidLinkToken {
  link_token: string;
  expiration: string;
}

export interface PlaidAccount {
  access_token: string;
  item_id: string;
}

export interface PlaidTransaction {
  transaction_id: string;
  date: string;
  name: string;
  amount: number;
  category?: string[];
  merchant_name?: string;
  payment_channel: string;
}
```

### 3. API Endpoints (`frontend/src/lib/api.ts`)
```typescript
plaidCreateLinkToken: `${API_BASE_URL}/api/plaid/create_link_token`
plaidExchangeToken: `${API_BASE_URL}/api/plaid/exchange_public_token`
plaidTransactions: `${API_BASE_URL}/api/plaid/transactions`
```

### 4. Connect Accounts Page (`frontend/src/pages/ConnectAccounts.tsx`)

#### Key Features:
- Fetches Plaid link token on component mount
- Uses `usePlaidLink` hook from react-plaid-link
- Opens Plaid Link UI when user clicks "Connect Account" for bank
- Handles successful connection by exchanging public token
- Fetches initial transaction data after connection
- Shows loading states and error handling
- Maintains connection status

#### Flow:
1. Component loads → Fetch link token from backend
2. User clicks "Connect Account" → Open Plaid Link UI
3. User authenticates with bank → Plaid returns public token
4. Exchange public token → Backend stores access token
5. Fetch transactions → Display success message
6. User can proceed to sync progress page

## Setup Instructions

### Backend Setup:

1. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Get Plaid credentials:
   - Sign up at https://dashboard.plaid.com/signup
   - Get your `client_id` and `secret` from the dashboard
   - Start with sandbox environment for testing

3. Configure environment variables in `.env`:
```env
PLAID_CLIENT_ID=your_actual_client_id
PLAID_SECRET=your_actual_secret
PLAID_ENV=sandbox
```

4. Run the backend:
```bash
uvicorn main:app --reload
```

### Frontend Setup:

1. Install dependencies:
```bash
cd frontend
pnpm install
```

2. Run the frontend:
```bash
pnpm dev
```

## Testing

### Sandbox Testing:
Plaid provides test credentials for sandbox environment:
- Username: `user_good`
- Password: `pass_good`
- Institution: Search for any bank (e.g., "Chase")

### Test Flow:
1. Navigate to Connect Accounts page
2. Click "Connect Account" on Bank Account card
3. Plaid Link UI opens
4. Select a test institution
5. Enter test credentials
6. Complete authentication
7. Verify success message
8. Check browser console for transaction data

## Security Considerations

1. **Access Token Storage**: Access tokens are stored encrypted in MongoDB
2. **Read-Only Access**: Plaid connections are read-only by default
3. **No Credential Storage**: User bank credentials never touch our servers
4. **Webhook Verification**: Implement webhook signature verification in production
5. **Token Rotation**: Implement access token rotation for long-term connections

## Production Checklist

- [ ] Switch from sandbox to production environment
- [ ] Update webhook URL to production domain
- [ ] Implement webhook signature verification
- [ ] Add error monitoring and logging
- [ ] Implement token refresh logic
- [ ] Add rate limiting for API endpoints
- [ ] Set up proper error handling for expired tokens
- [ ] Implement transaction sync scheduling
- [ ] Add user notification for connection issues
- [ ] Test with real bank accounts

## Transaction Data Structure

Plaid returns transactions with the following structure:
```json
{
  "transaction_id": "unique_id",
  "date": "2024-01-15",
  "name": "Merchant Name",
  "amount": 42.50,
  "category": ["Food and Drink", "Restaurants"],
  "merchant_name": "Starbucks",
  "payment_channel": "in store"
}
```

This data can be mapped to your internal transaction format for classification and analysis.

## Troubleshooting

### Common Issues:

1. **Link token creation fails**
   - Verify Plaid credentials in .env
   - Check API endpoint is accessible
   - Ensure user is authenticated

2. **Plaid Link doesn't open**
   - Check browser console for errors
   - Verify link token is valid and not expired
   - Ensure react-plaid-link is properly installed

3. **Token exchange fails**
   - Verify backend endpoint is accessible
   - Check public token is being sent correctly
   - Review backend logs for Plaid API errors

4. **No transactions returned**
   - Verify access token is stored correctly
   - Check date range parameters
   - Ensure bank account has transactions in the period

## Next Steps

1. Implement transaction categorization using Plaid categories
2. Set up automatic transaction syncing via webhooks
3. Add support for multiple bank accounts per user
4. Implement balance tracking and alerts
5. Add transaction search and filtering
6. Create transaction reconciliation features
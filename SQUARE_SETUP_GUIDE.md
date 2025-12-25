# Square POS Integration Setup Guide

This guide will help you set up Square API integration for FinSense AI to enable sales and payment data synchronization from your Square Point of Sale system.

## Overview

FinSense AI uses Square OAuth to securely connect to users' Square accounts and fetch transaction data, including sales, payments, and customer information. The integration supports both Sandbox mode (for development/testing) and Production mode (for live data).

## Prerequisites

- A Square account (sign up at https://squareup.com)
- Access to Square Developer Dashboard
- FinSense AI backend running locally or deployed

## Step 1: Create a Square Application

1. **Log in to Square Developer Dashboard**
   - Go to https://developer.squareup.com/apps
   - Sign in with your Square account

2. **Create a New Application**
   - Click "+" or "Create App" button
   - Enter application details:
     - **Application name**: FinSense AI
     - **Description**: Financial management platform for small businesses
   - Click "Save"

3. **Note Your Application ID**
   - After creating the app, you'll see your Application ID
   - This will be used as your `SQUARE_APPLICATION_ID`

## Step 2: Configure OAuth Settings

1. **Navigate to OAuth Settings**
   - In your Square application dashboard
   - Click on "OAuth" in the left sidebar

2. **Add Redirect URL**
   - Under "Redirect URL", add:
     - For development: `http://localhost:5137/square/callback`
     - For production: `https://yourdomain.com/square/callback`
   - Click "Save"

3. **Configure Permissions**
   - Under "Permissions", select the following:
     - ✅ `PAYMENTS_READ` - Read payment information
     - ✅ `ORDERS_READ` - Read order information
     - ✅ `MERCHANT_PROFILE_READ` - Read merchant profile
     - ✅ `CUSTOMERS_READ` - Read customer information (optional)
   - Click "Save"

## Step 3: Get Your Square Credentials

### For Sandbox Mode (Development/Testing)

1. **Switch to Sandbox**
   - In the Square Developer Dashboard
   - Toggle to "Sandbox" mode (usually in the top right)

2. **Get Sandbox Credentials**
   - Go to "Credentials" tab
   - Copy the following:
     - **Sandbox Application ID** (starts with `sandbox-sq0idb-`)
     - **Sandbox Access Token** (starts with `sandbox-sq0atb-`)

### For Production Mode (Live Data)

1. **Complete Account Verification**
   - Ensure your Square account is fully verified
   - Complete any required business information

2. **Switch to Production**
   - Toggle to "Production" mode in the dashboard

3. **Get Production Credentials**
   - Go to "Credentials" tab
   - Copy the following:
     - **Production Application ID** (starts with `sq0idp-`)
     - **Production Access Token** (starts with `sq0atp-`)

## Step 4: Configure FinSense AI Backend

1. **Open your `.env` file** in the `backend` directory

2. **Add Square credentials**:

   For Sandbox Mode:
   ```env
   # Square Configuration (Sandbox Mode)
   SQUARE_APPLICATION_ID=sandbox-sq0idb-XXXXXXXXXXXXXXXXXXXXXXXX
   SQUARE_ACCESS_TOKEN=sandbox-sq0atb-XXXXXXXXXXXXXXXXXXXXXXXX
   SQUARE_ENVIRONMENT=sandbox
   SQUARE_WEBHOOK_SIGNATURE_KEY=XXXXXXXXXXXXXXXXXXXXXXXX
   ```

   For Production Mode:
   ```env
   # Square Configuration (Production Mode)
   SQUARE_APPLICATION_ID=sq0idp-XXXXXXXXXXXXXXXXXXXXXXXX
   SQUARE_ACCESS_TOKEN=sq0atp-XXXXXXXXXXXXXXXXXXXXXXXX
   SQUARE_ENVIRONMENT=production
   SQUARE_WEBHOOK_SIGNATURE_KEY=XXXXXXXXXXXXXXXXXXXXXXXX
   ```

3. **Save the file**

## Step 5: Install Square SDK (if not already installed)

```bash
cd backend
pip install squareup
```

## Step 6: Set Up Webhooks (Optional but Recommended)

Webhooks allow Square to notify your application about events like new payments, refunds, etc.

1. **Create a Webhook Subscription**
   - In Square Developer Dashboard, go to "Webhooks"
   - Click "Add Subscription"
   - Enter your endpoint URL:
     - For development: `http://localhost:8000/api/square/webhook`
     - For production: `https://yourdomain.com/api/square/webhook`

2. **Select Events to Subscribe To**
   - Select the following events:
     - `payment.created`
     - `payment.updated`
     - `order.created`
     - `order.updated`
     - `refund.created`
     - `refund.updated`

3. **Get Webhook Signature Key**
   - After creating the subscription, you'll see a "Signature Key"
   - Copy this key
   - Add it to your `.env` file as `SQUARE_WEBHOOK_SIGNATURE_KEY`

4. **Enable the Webhook**
   - Toggle the webhook to "Enabled"
   - Click "Save"

## Step 7: Test the Integration

1. **Restart the Backend Server**
   ```bash
   cd backend
   python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

2. **Start the Frontend**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Test Square Connection**
   - Open http://localhost:5137 in your browser
   - Sign in or create an account
   - Navigate to "Connect Accounts" page
   - Click "Connect Account" on the Square POS card
   - You should be redirected to Square OAuth page
   - Authorize the connection
   - You'll be redirected back to FinSense AI

4. **Verify Connection**
   - After successful connection, the Square card should show "Connected"
   - You can now fetch transaction data from your Square account

## Step 8: Testing with Sandbox Mode

When using Square Sandbox mode, you can create test transactions:

### Using Square Sandbox Dashboard

1. **Access Sandbox Dashboard**
   - Go to https://developer.squareup.com/apps
   - Select your application
   - Click "Sandbox Test Accounts"

2. **Create Test Transactions**
   - Use the Sandbox Dashboard to create test payments
   - These will appear in your FinSense AI application

### Test Payment Methods

Square Sandbox accepts these test card numbers:

- **Successful payment**: `4111 1111 1111 1111` (Visa)
- **Successful payment**: `5105 1051 0510 5100` (Mastercard)
- **Card declined**: `4000 0000 0000 0002`
- **Insufficient funds**: `4000 0000 0000 9995`

**Test Details:**
- **Expiry**: Any future date (e.g., 12/25)
- **CVV**: Any 3 digits (e.g., 123)
- **ZIP**: Any 5 digits (e.g., 12345)

## Troubleshooting

### Issue: "Invalid application ID"
- **Solution**: Verify you're using the correct Application ID from Square Developer Dashboard
- Make sure you're using the right environment (sandbox vs production)

### Issue: "Redirect URI mismatch"
- **Solution**: Ensure the redirect URI in Square OAuth settings matches exactly:
  - Development: `http://localhost:5137/square/callback`
  - Check for trailing slashes and http vs https

### Issue: "Insufficient permissions"
- **Solution**: Go to Square Developer Dashboard → OAuth → Permissions
- Ensure you've enabled: `PAYMENTS_READ`, `ORDERS_READ`, `MERCHANT_PROFILE_READ`

### Issue: "No Square account connected"
- **Solution**: Complete the OAuth flow by clicking "Connect Account" and authorizing on Square

### Issue: Mock mode is being used instead of real Square
- **Solution**: Check that your `.env` file has valid Square credentials
- The backend will use mock mode if:
  - `SQUARE_APPLICATION_ID` is empty
  - `SQUARE_APPLICATION_ID` equals "your-square-application-id"
  - `SQUARE_APPLICATION_ID` starts with "your-square-"

### Issue: "Access token expired"
- **Solution**: Square access tokens don't expire, but if you regenerate them:
  - Get the new access token from Square Developer Dashboard
  - Update your `.env` file
  - Restart the backend server

## Security Best Practices

1. **Never commit credentials to version control**
   - Keep `.env` file in `.gitignore`
   - Use environment variables in production

2. **Use Sandbox Mode for Development**
   - Always use sandbox credentials during development
   - Only use production credentials in production environment

3. **Rotate Access Tokens Regularly**
   - Regenerate access tokens periodically
   - Immediately regenerate if you suspect a token has been compromised

4. **Verify Webhook Signatures**
   - Always verify webhook signatures using the signature key
   - This prevents unauthorized webhook calls

5. **Use HTTPS in Production**
   - Always use HTTPS for redirect URIs and webhook endpoints in production
   - Square requires HTTPS for production webhooks

## API Endpoints

Once configured, the following Square endpoints will be available:

- `GET /api/square/authorize` - Get OAuth authorization URL
- `GET /api/square/callback` - Handle OAuth callback
- `GET /api/square/locations` - Get merchant locations
- `GET /api/square/payments` - Fetch payment transactions
- `GET /api/square/orders` - Fetch order data
- `GET /api/square/customers` - Fetch customer information
- `POST /api/square/webhook` - Handle Square webhooks
- `DELETE /api/square/disconnect` - Disconnect Square account

## Data Synchronization

### What Data is Synced?

- **Payments**: All payment transactions with amounts, dates, and payment methods
- **Orders**: Order details including items, quantities, and totals
- **Refunds**: Refund transactions and amounts
- **Customers**: Customer information (if permission granted)
- **Locations**: Store/location information

### Sync Frequency

- **Initial Sync**: Last 90 days of transaction history
- **Ongoing Sync**: Real-time via webhooks (if configured)
- **Manual Sync**: Available through the dashboard

## Square API Limits

Be aware of Square API rate limits:

- **Production**: 500 requests per minute per location
- **Sandbox**: 100 requests per minute
- The application handles rate limiting automatically with retries

## Additional Resources

- [Square Developer Documentation](https://developer.squareup.com/docs)
- [Square OAuth Guide](https://developer.squareup.com/docs/oauth-api/overview)
- [Square API Reference](https://developer.squareup.com/reference/square)
- [Square Webhooks Guide](https://developer.squareup.com/docs/webhooks/overview)
- [Square Sandbox Testing](https://developer.squareup.com/docs/testing/sandbox)

## Support

If you encounter any issues:

1. Check the backend terminal for error messages
2. Verify all credentials are correct in `.env`
3. Ensure redirect URIs match exactly in Square OAuth settings
4. Check Square Developer Dashboard for OAuth errors
5. Review Square API logs in the Developer Dashboard
6. Verify you have the required permissions enabled
7. Review this guide for common troubleshooting steps

## Differences Between Square and Other Integrations

### Square vs Stripe
- **Square**: Best for retail/POS transactions, in-person payments
- **Stripe**: Best for online payments, subscriptions

### Square vs Plaid
- **Square**: Payment processing data (what you sold)
- **Plaid**: Bank account data (all business transactions)

### When to Use Square
- You use Square POS for in-person sales
- You want to track retail transactions
- You need detailed order and item-level data
- You want to sync customer purchase history

---

**Note**: This integration uses Square OAuth for secure, read-only access to transaction data. Users maintain full control and can disconnect at any time. Square access tokens do not expire but can be revoked by the user at any time through their Square account settings.
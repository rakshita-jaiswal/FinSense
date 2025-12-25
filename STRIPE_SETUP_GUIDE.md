# Stripe Integration Setup Guide

This guide will help you set up Stripe Connect integration for FinSense AI to enable payment processing data synchronization.

## Overview

FinSense uses Stripe Connect OAuth to securely connect to users' Stripe accounts and fetch payment transaction data. The integration supports both test mode (for development) and live mode (for production).

## Prerequisites

- A Stripe account (sign up at https://stripe.com)
- Access to Stripe Dashboard
- FinSense AI backend running locally or deployed

## Step 1: Create a Stripe Connect Application

1. **Log in to Stripe Dashboard**
   - Go to https://dashboard.stripe.com
   - Sign in with your Stripe account

2. **Navigate to Connect Settings**
   - Click on "Developers" in the left sidebar
   - Click on "Connect" under the Developers section
   - Or go directly to: https://dashboard.stripe.com/settings/applications

3. **Create a Connect Platform**
   - If you haven't created a platform yet, click "Get started"
   - Fill in your platform information:
     - **Platform name**: FinSense AI
     - **Platform website**: Your application URL (e.g., http://localhost:5137 for development)
     - **Support email**: Your support email address

4. **Configure OAuth Settings**
   - Under "Integration" tab, find "OAuth settings"
   - Add your redirect URI:
     - For development: `http://localhost:5137/stripe/callback`
     - For production: `https://yourdomain.com/stripe/callback`
   - Click "Save changes"

## Step 2: Get Your Stripe Credentials

### For Test Mode (Development)

1. **Get Test Mode Credentials**
   - In the Stripe Dashboard, make sure you're in "Test mode" (toggle in the top right)
   - Go to "Developers" → "API keys"
   - Copy your **Publishable key** (starts with `pk_test_`)
   - Click "Reveal test key" and copy your **Secret key** (starts with `sk_test_`)

2. **Get Connect Client ID**
   - Go to "Developers" → "Connect" → "Settings"
   - Under "OAuth settings", find your **Test mode client ID** (starts with `ca_`)
   - Copy this Client ID

### For Live Mode (Production)

1. **Activate Your Account**
   - Complete Stripe account activation if not already done
   - Provide business information and bank account details

2. **Get Live Mode Credentials**
   - Switch to "Live mode" in the Stripe Dashboard
   - Go to "Developers" → "API keys"
   - Copy your **Publishable key** (starts with `pk_live_`)
   - Click "Reveal live key" and copy your **Secret key** (starts with `sk_live_`)

3. **Get Live Connect Client ID**
   - Go to "Developers" → "Connect" → "Settings"
   - Under "OAuth settings", find your **Live mode client ID** (starts with `ca_`)
   - Copy this Client ID

## Step 3: Configure FinSense AI Backend

1. **Open your `.env` file** in the `backend` directory

2. **Add Stripe credentials**:

   For Test Mode:
   ```env
   # Stripe Configuration (Test Mode)
   STRIPE_SECRET_KEY=sk_test_your_secret_key_here
   STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key_here
   STRIPE_CLIENT_ID=ca_your_client_id_here
   STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here
   ```

   For Live Mode:
   ```env
   # Stripe Configuration (Live Mode)
   STRIPE_SECRET_KEY=sk_live_your_secret_key_here
   STRIPE_PUBLISHABLE_KEY=pk_live_your_publishable_key_here
   STRIPE_CLIENT_ID=ca_your_client_id_here
   STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here
   ```

3. **Save the file**

## Step 4: Set Up Webhooks (Optional but Recommended)

Webhooks allow Stripe to notify your application about events like successful payments, refunds, etc.

1. **Create a Webhook Endpoint**
   - In Stripe Dashboard, go to "Developers" → "Webhooks"
   - Click "Add endpoint"
   - Enter your endpoint URL:
     - For development: `http://localhost:8000/api/stripe/webhook`
     - For production: `https://yourdomain.com/api/stripe/webhook`

2. **Select Events to Listen To**
   - Select the following events:
     - `charge.succeeded`
     - `charge.refunded`
     - `payment_intent.succeeded`
     - `payment_intent.payment_failed`

3. **Get Webhook Secret**
   - After creating the webhook, click on it
   - Click "Reveal" next to "Signing secret"
   - Copy the webhook secret (starts with `whsec_`)
   - Add it to your `.env` file as `STRIPE_WEBHOOK_SECRET`

## Step 5: Test the Integration

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

3. **Test Stripe Connection**
   - Open http://localhost:5137 in your browser
   - Sign in or create an account
   - Navigate to "Connect Accounts" page
   - Click "Connect Account" on the Stripe card
   - You should be redirected to Stripe OAuth page
   - Authorize the connection
   - You'll be redirected back to FinSense AI

4. **Verify Connection**
   - After successful connection, the Stripe card should show "Connected"
   - You can now fetch payment data from your Stripe account

## Step 6: Testing with Test Mode

When using Stripe Test Mode, you can use test payment methods:

### Test Card Numbers
- **Successful payment**: `4242 4242 4242 4242`
- **Requires authentication**: `4000 0025 0000 3155`
- **Declined card**: `4000 0000 0000 0002`

### Test Details
- **Expiry**: Any future date (e.g., 12/34)
- **CVC**: Any 3 digits (e.g., 123)
- **ZIP**: Any 5 digits (e.g., 12345)

## Troubleshooting

### Issue: "Invalid client_id"
- **Solution**: Make sure you're using the correct Client ID from Stripe Connect settings
- Verify you're using the right mode (test vs live)

### Issue: "Redirect URI mismatch"
- **Solution**: Ensure the redirect URI in your Stripe Connect settings matches exactly:
  - Development: `http://localhost:5137/stripe/callback`
  - Check for trailing slashes and http vs https

### Issue: "No Stripe account connected"
- **Solution**: Complete the OAuth flow by clicking "Connect Account" and authorizing on Stripe

### Issue: Mock mode is being used instead of real Stripe
- **Solution**: Check that your `.env` file has valid Stripe credentials
- The backend will use mock mode if:
  - `STRIPE_CLIENT_ID` is empty
  - `STRIPE_CLIENT_ID` equals "ca_your-stripe-client-id"
  - `STRIPE_CLIENT_ID` starts with "ca_your-"

## Security Best Practices

1. **Never commit credentials to version control**
   - Keep `.env` file in `.gitignore`
   - Use environment variables in production

2. **Use Test Mode for Development**
   - Always use test mode credentials during development
   - Only use live mode in production

3. **Rotate Keys Regularly**
   - Rotate your API keys periodically
   - Immediately rotate if you suspect a key has been compromised

4. **Verify Webhook Signatures**
   - Always verify webhook signatures using the webhook secret
   - This prevents unauthorized webhook calls

## API Endpoints

Once configured, the following Stripe endpoints are available:

- `GET /api/stripe/authorize` - Get OAuth authorization URL
- `GET /api/stripe/callback` - Handle OAuth callback
- `GET /api/stripe/account` - Get connected account info
- `GET /api/stripe/charges` - Fetch payment charges
- `GET /api/stripe/payment-intents` - Fetch payment intents
- `POST /api/stripe/webhook` - Handle Stripe webhooks
- `DELETE /api/stripe/disconnect` - Disconnect Stripe account

## Additional Resources

- [Stripe Connect Documentation](https://stripe.com/docs/connect)
- [Stripe OAuth Documentation](https://stripe.com/docs/connect/oauth-reference)
- [Stripe API Reference](https://stripe.com/docs/api)
- [Stripe Testing Guide](https://stripe.com/docs/testing)

## Support

If you encounter any issues:
1. Check the backend terminal for error messages
2. Verify all credentials are correct in `.env`
3. Ensure redirect URIs match exactly
4. Check Stripe Dashboard logs for OAuth errors
5. Review this guide for common troubleshooting steps

---

**Note**: This integration uses Stripe Connect with OAuth for secure, read-only access to payment data. Users maintain full control and can disconnect at any time.
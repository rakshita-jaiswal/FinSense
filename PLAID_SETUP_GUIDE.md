# Plaid Integration Setup Guide

## Current Issue
The "Failed to initialize bank connection" error occurs because the application needs valid Plaid API credentials to connect to bank accounts.

## Solution: Get Plaid Credentials

### Step 1: Sign Up for Plaid
1. Go to [Plaid Dashboard](https://dashboard.plaid.com/signup)
2. Create a free account (Sandbox environment is free)
3. Complete the registration process

### Step 2: Get Your Credentials
1. Log in to the [Plaid Dashboard](https://dashboard.plaid.com/)
2. Navigate to **Team Settings** → **Keys**
3. Copy your credentials:
   - **client_id**: Your Plaid Client ID
   - **sandbox secret**: Your Sandbox Secret Key

### Step 3: Update Environment Variables
Update your `backend/.env` file with the actual credentials:

```env
# Plaid Configuration
PLAID_CLIENT_ID=your_actual_client_id_here
PLAID_SECRET=your_actual_sandbox_secret_here
PLAID_ENV=sandbox
```

### Step 4: Restart the Backend Server
After updating the credentials, restart your backend server:
```bash
cd backend
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## Plaid Environments

- **Sandbox**: Free, uses test data, perfect for development
- **Development**: For testing with real bank credentials (limited transactions)
- **Production**: For live applications (requires approval and fees)

## Testing in Sandbox Mode

When using Sandbox credentials, you can test with these credentials:
- **Username**: `user_good`
- **Password**: `pass_good`
- **Institution**: Any test bank from the Plaid Link flow

## Important Notes

1. **Never commit real credentials** to version control
2. Keep your `.env` file in `.gitignore`
3. Sandbox is completely free and perfect for development
4. You can create unlimited test accounts in Sandbox mode

## Troubleshooting

If you still see "Failed to initialize bank connection":
1. Verify your credentials are correct in `.env`
2. Ensure the backend server restarted after updating `.env`
3. Check the backend terminal for any error messages
4. Verify you're using the Sandbox secret (not Development or Production)

## Additional Resources

- [Plaid Quickstart Guide](https://plaid.com/docs/quickstart/)
- [Plaid API Documentation](https://plaid.com/docs/api/)
- [Plaid Sandbox Testing](https://plaid.com/docs/sandbox/)
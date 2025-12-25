# Sample Data Seeding Guide

This guide explains how to populate your MongoDB database with sample data for testing and development.

## Overview

The `seed_sample_data.py` script creates realistic sample data including:
- **Test User Account**: A pre-configured user for testing
- **3 Connected Accounts**: Square POS, Stripe Payments, and Chase Business Checking
- **75 Sample Transactions**: Mix of revenue and expenses over the last 30 days
- **Realistic Financial Data**: Proper categorization with AI confidence scores

## Prerequisites

1. MongoDB Atlas connection configured in `.env` file
2. Python dependencies installed (`pip install -r requirements.txt`)
3. Backend environment variables set up

## Usage

### Running the Script

```bash
cd backend
python seed_sample_data.py
```

### What the Script Does

1. **Connects to MongoDB** using credentials from `.env`
2. **Checks for existing test user** (`test@example.com`)
   - If exists: Uses existing user
   - If not: Creates new test user
3. **Checks for existing data**
   - If data exists: Prompts to delete and reseed
   - If no data: Proceeds with seeding
4. **Creates sample data**:
   - 3 connected accounts (Square, Stripe, Bank)
   - ~30 revenue transactions ($50-$800 each)
   - ~45 expense transactions across multiple categories
   - Realistic dates spread over last 30 days

### Sample Data Details

#### Test User Credentials
- **Email**: `test@example.com`
- **Password**: `Test123!@#`
- **Business**: Test Business LLC

#### Connected Accounts
1. **Square POS** - Point of sale system
2. **Stripe Payments** - Online payment processing
3. **Chase Business Checking** - Bank account

#### Transaction Categories

**Revenue** (~$12,000-$18,000 total):
- Daily Sales
- Online Orders
- Catering Service
- Gift Card Sales
- Delivery Orders
- Event Bookings

**Expenses** (~$8,000-$15,000 total):
- Inventory - Food & Supplies (Sysco, US Foods, Restaurant Depot)
- Payroll (Square Payroll, ADP)
- Utilities (Con Edison, National Grid, Verizon)
- Marketing (Facebook Ads, Google Ads)
- Office Supplies (Amazon Business, Staples)
- Professional Fees (Insurance)
- Repairs & Maintenance

#### AI Confidence Scores
- Revenue transactions: 0.92-0.99 (high confidence)
- Expense transactions: 0.75-0.95 (varied confidence)
- Transactions with confidence > 0.85 are auto-approved
- Lower confidence transactions marked as "needs-review"

## Expected Output

```
============================================================
SEEDING SAMPLE DATA INTO MONGODB
============================================================

[OK] Using existing test user: test@example.com
  User ID: 693f45e1f904afe4a3c88428

============================================================
CREATING CONNECTED ACCOUNTS
============================================================
[OK] Created 3 connected accounts:
  - Square POS (square)
  - Stripe Payments (stripe)
  - Chase Business Checking (bank)

============================================================
GENERATING SAMPLE TRANSACTIONS
============================================================

Generating revenue transactions...
Generating expense transactions...

[OK] Created 75 transactions

============================================================
SUMMARY
============================================================

User: test@example.com
User ID: 693f45e1f904afe4a3c88428

Connected Accounts: 3
  - Square POS
  - Stripe Payments
  - Chase Business Checking

Transactions: 75
  - Revenue: 30 transactions ($15,234.56)
  - Expenses: 45 transactions ($11,789.23)
  - Net Profit: $3,445.33

============================================================
SAMPLE DATA SEEDED SUCCESSFULLY!
============================================================

You can now login with:
  Email: test@example.com
  Password: Test123!@#
```

## Testing the Data

After seeding, you can:

1. **Login to the application**:
   - Email: `test@example.com`
   - Password: `Test123!@#`

2. **View Dashboard**: See financial statistics and charts populated with real data

3. **Browse Transactions**: Review the 75 sample transactions

4. **Test Filtering**: Filter by category, date range, or search vendors

5. **Check Analytics**: View revenue trends, expense breakdowns, and alerts

## Reseeding Data

If you want to reseed with fresh data:

1. Run the script: `python seed_sample_data.py`
2. When prompted "Delete existing data and reseed? (y/n):", type `y`
3. The script will delete old data and create new sample data

## Troubleshooting

### Connection Error
```
ServerSelectionTimeoutError: localhost:27017
```
**Solution**: Check that `MONGODB_URI` in `.env` points to your MongoDB Atlas cluster

### Unicode Error
```
UnicodeEncodeError: 'charmap' codec can't encode character
```
**Solution**: Script has been updated to use ASCII characters only

### User Already Exists
The script will use the existing test user and prompt before overwriting data.

## Notes

- Sample data is generated with random amounts and dates
- Each run creates slightly different data due to randomization
- Data is realistic and suitable for demos and testing
- All transactions have proper categorization and confidence scores
- The script is safe to run multiple times

## Integration with Application

This sample data works seamlessly with:
- Dashboard analytics endpoints
- Transaction management features
- Category filtering
- Search functionality
- Financial reporting
- AI assistant queries

## Future Enhancements

Potential improvements:
- Command-line arguments for customization
- Multiple test users
- Configurable date ranges
- Industry-specific templates
- Bulk data generation for stress testing
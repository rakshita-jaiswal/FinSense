# 📊 Sample Data Setup Guide for FinSense AI

> **Quick Start**: Run `cd backend && python seed_sample_data.py` to populate your database with realistic test data in under 30 seconds.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [What Gets Created](#what-gets-created)
- [Usage Guide](#usage-guide)
- [Testing Your Data](#testing-your-data)
- [Troubleshooting](#troubleshooting)
- [Advanced Options](#advanced-options)

---

## 🎯 Overview

The sample data seeding system creates a complete, realistic financial dataset for testing and development. This includes:

| Component | Count | Description |
|-----------|-------|-------------|
| **Test User** | 1 | Pre-configured account with secure credentials |
| **Connected Accounts** | 3 | Square POS, Stripe Payments, Chase Business Checking |
| **Sample Transactions** | 75 | Mix of revenue and expenses over 30 days |
| **Financial Data** | ~$15K revenue, ~$12K expenses | Realistic amounts with proper categorization |

### Key Features

✅ **Realistic Data**: Industry-standard vendors, amounts, and patterns  
✅ **AI Confidence Scores**: Simulates ML categorization (0.75-0.99)  
✅ **Auto-Approval Logic**: High-confidence transactions auto-approved  
✅ **Safe Reseeding**: Prompts before overwriting existing data  
✅ **Idempotent**: Safe to run multiple times  

---

## ✅ Prerequisites

Before running the seeding script, ensure you have:

### 1. MongoDB Atlas Connection

Your [`backend/.env`](backend/.env.example) file must contain:

```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/finsense?retryWrites=true&w=majority
```

> 💡 **Tip**: See [`MONGODB_SETUP_GUIDE.md`](MONGODB_SETUP_GUIDE.md) for detailed setup instructions.

### 2. Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

Required packages:
- `motor` - Async MongoDB driver
- `passlib[argon2]` - Password hashing
- `python-dotenv` - Environment variable management

### 3. Database Access

Verify your MongoDB connection:

```bash
cd backend
python -c "from motor.motor_asyncio import AsyncIOMotorClient; import os; from dotenv import load_dotenv; load_dotenv(); print('✓ Connection successful' if os.getenv('MONGODB_URI') else '✗ MONGODB_URI not found')"
```

---

## 🚀 Quick Start

### Option 1: Standalone Script (Recommended)

```bash
cd backend
python seed_sample_data.py
```

**Expected output:**
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

### Option 2: Auto-Seed on User Signup

Sample data can be automatically created when new users sign up. This is controlled in [`backend/services/sample_data_seeder.py`](backend/services/sample_data_seeder.py:148).

---

## 📦 What Gets Created

### 1. Test User Account

| Field | Value |
|-------|-------|
| **Email** | `test@example.com` |
| **Password** | `Test123!@#` |
| **First Name** | Test |
| **Last Name** | User |
| **Business Name** | Test Business LLC |

> 🔒 **Security**: Password is hashed using Argon2 algorithm.

### 2. Connected Accounts (3)

#### Square POS
- **Source**: `square`
- **Purpose**: Point of sale transactions
- **Typical Transactions**: Daily sales, catering, events

#### Stripe Payments
- **Source**: `stripe`
- **Purpose**: Online payment processing
- **Typical Transactions**: Online orders, subscriptions, gift cards

#### Chase Business Checking
- **Source**: `bank`
- **Purpose**: Bank account transactions
- **Typical Transactions**: Deposits, ACH transfers, checks

### 3. Sample Transactions (75)

#### Revenue Transactions (30) - ~$15,000 total

| Vendor Type | Count | Amount Range | Confidence |
|-------------|-------|--------------|------------|
| Daily Sales | 5-8 | $50-$800 | 0.92-0.99 |
| Online Orders | 5-8 | $50-$800 | 0.92-0.99 |
| Catering Service | 3-5 | $50-$800 | 0.92-0.99 |
| Gift Card Sales | 2-4 | $50-$800 | 0.92-0.99 |
| Delivery Orders | 3-5 | $50-$800 | 0.92-0.99 |
| Event Bookings | 2-4 | $50-$800 | 0.92-0.99 |

**Status**: All auto-approved (high confidence)

#### Expense Transactions (45) - ~$12,000 total

| Category | Vendors | Amount Range | Confidence |
|----------|---------|--------------|------------|
| **Inventory - Food & Supplies** | Sysco, US Foods, Restaurant Depot | $150-$800 | 0.75-0.95 |
| **Payroll** | Square Payroll, ADP | $1,800-$4,000 | 0.75-0.95 |
| **Utilities** | Con Edison, National Grid, Verizon | $100-$400 | 0.75-0.95 |
| **Marketing** | Facebook Ads, Google Ads | $100-$600 | 0.75-0.95 |
| **Office Supplies** | Amazon Business, Staples | $30-$250 | 0.75-0.95 |
| **Professional Fees** | State Farm Insurance | $200-$500 | 0.75-0.95 |
| **Repairs & Maintenance** | Equipment Repair Co | $100-$800 | 0.75-0.95 |

**Status**: 
- Confidence > 0.85: Auto-approved
- Confidence ≤ 0.85: Needs review

### 4. AI Categorization Details

Each transaction includes:

```typescript
{
  category: string,           // e.g., "Revenue", "Payroll", "Utilities"
  confidence: number,         // 0.75-0.99 (AI confidence score)
  status: string,             // "auto-approved" or "needs-review"
  explanation: string,        // Human-readable categorization reason
  payment_method: string,     // e.g., "Square POS", "Business Debit"
  original_description: string // Raw transaction description
}
```

---

## 🧪 Testing Your Data

### 1. Login to Application

Navigate to your frontend (typically `http://localhost:5173`) and login:

```
Email: test@example.com
Password: Test123!@#
```

### 2. Verify Dashboard

Check that the dashboard displays:
- ✅ Total revenue (~$15,000)
- ✅ Total expenses (~$12,000)
- ✅ Net profit (~$3,000)
- ✅ Revenue trend chart with data points
- ✅ Expense breakdown by category

### 3. Browse Transactions

Navigate to **Transactions** page and verify:
- ✅ 75 total transactions listed
- ✅ Mix of revenue (negative amounts) and expenses (positive amounts)
- ✅ Proper categorization
- ✅ Confidence scores displayed
- ✅ Some transactions marked "needs-review"

### 4. Test Filtering

Try these filters:
- **By Category**: Select "Payroll" → Should show 2-4 transactions
- **By Date Range**: Last 7 days → Should show ~17-20 transactions
- **By Status**: "Needs Review" → Should show ~10-15 transactions
- **Search**: "Sysco" → Should show food supply transactions

### 5. Check Connected Accounts

Navigate to **Connect Accounts** page:
- ✅ 3 accounts shown as connected
- ✅ Square POS, Stripe Payments, Chase Business Checking
- ✅ Connection dates ~30 days ago

---

## 🔧 Troubleshooting

### Issue: Connection Timeout

```
ServerSelectionTimeoutError: localhost:27017
```

**Solution**: 
1. Verify `MONGODB_URI` in [`backend/.env`](backend/.env.example) points to MongoDB Atlas (not localhost)
2. Check MongoDB Atlas network access allows your IP
3. Verify credentials are correct

### Issue: User Already Exists

```
[WARNING] User already has 3 connected accounts
Delete existing data and reseed? (y/n):
```

**Solution**: 
- Type `y` to delete and reseed with fresh data
- Type `n` to keep existing data and abort

### Issue: Unicode Encoding Error

```
UnicodeEncodeError: 'charmap' codec can't encode character
```

**Solution**: This has been fixed in the latest version. All vendor names use ASCII characters only.

### Issue: Import Error

```
ModuleNotFoundError: No module named 'motor'
```

**Solution**:
```bash
cd backend
pip install -r requirements.txt
```

### Issue: No Data Appears in Dashboard

**Checklist**:
1. ✅ Script completed successfully (check terminal output)
2. ✅ Logged in with correct credentials (`test@example.com`)
3. ✅ Backend server is running (`python -m uvicorn main:app --reload`)
4. ✅ Frontend is connected to correct backend URL
5. ✅ Check browser console for API errors

---

## 🔄 Reseeding Data

### When to Reseed

- Testing new features that modify transactions
- After database schema changes
- When you need fresh randomized data
- Corrupted or inconsistent test data

### How to Reseed

```bash
cd backend
python seed_sample_data.py
```

When prompted:
```
Delete existing data and reseed? (y/n): y
```

This will:
1. Delete all existing connected accounts for test user
2. Delete all existing transactions for test user
3. Create fresh sample data with new random values

> ⚠️ **Warning**: This only affects the test user (`test@example.com`). Other users' data is not touched.

---

## 🎛️ Advanced Options

### Customizing Transaction Counts

Edit [`backend/seed_sample_data.py`](backend/seed_sample_data.py:120):

```python
# Change these values:
for _ in range(30):  # Revenue transactions (line 120)
for _ in range(45):  # Expense transactions (line 158)
```

### Customizing Date Range

Edit [`backend/seed_sample_data.py`](backend/seed_sample_data.py:122):

```python
# Change from 30 days to 90 days:
days_ago = random.randint(0, 90)  # Line 122 and 159
```

### Adding Custom Vendors

Edit [`backend/seed_sample_data.py`](backend/seed_sample_data.py:114):

```python
revenue_vendors = [
    "Daily Sales", "Online Orders", "Your Custom Vendor",
    # Add more vendors here
]
```

### Customizing Amount Ranges

Edit [`backend/seed_sample_data.py`](backend/seed_sample_data.py:128):

```python
# Change revenue amounts:
amount = -round(random.uniform(100, 1500), 2)  # Line 128

# Change expense amounts in expense_categories tuple:
("Sysco", "Inventory - Food & Supplies", 500, 2000),  # Line 141
```

### Creating Multiple Test Users

Modify [`backend/seed_sample_data.py`](backend/seed_sample_data.py:36) to create additional users:

```python
test_users = [
    ("test@example.com", "Test123!@#", "Test Business LLC"),
    ("demo@example.com", "Demo123!@#", "Demo Restaurant"),
    ("sample@example.com", "Sample123!@#", "Sample Cafe")
]
```

---

## 📚 Related Documentation

- [`backend/README_SAMPLE_DATA.md`](backend/README_SAMPLE_DATA.md) - Detailed backend documentation
- [`MONGODB_SETUP_GUIDE.md`](MONGODB_SETUP_GUIDE.md) - MongoDB Atlas setup
- [`backend/services/sample_data_seeder.py`](backend/services/sample_data_seeder.py) - Auto-seed service
- [`backend/services/transaction_generator.py`](backend/services/transaction_generator.py) - Transaction generation logic

---

## 🤝 Integration with Application

The sample data integrates seamlessly with:

| Feature | Integration |
|---------|-------------|
| **Dashboard Analytics** | Revenue/expense calculations, trend charts |
| **Transaction Management** | Listing, filtering, searching, categorization |
| **Category System** | Pre-categorized with confidence scores |
| **Search Functionality** | Vendor name and description search |
| **Financial Reporting** | Profit/loss calculations, period comparisons |
| **AI Assistant** | Query historical transaction data |
| **Review Queue** | Low-confidence transactions for manual review |

---

## 🚀 Future Enhancements

Planned improvements:

- [ ] CLI arguments for customization (`--transactions=100 --days=60`)
- [ ] Multiple test user profiles (restaurant, retail, services)
- [ ] Configurable industry templates
- [ ] Bulk data generation for performance testing
- [ ] Export/import sample data sets
- [ ] Seasonal transaction patterns
- [ ] Multi-currency support
- [ ] Recurring transaction patterns

---

## 📝 Notes

- Sample data uses **randomization** - each run creates slightly different amounts and dates
- All transactions have **realistic categorization** with AI confidence scores
- The script is **idempotent** - safe to run multiple times
- Data is suitable for **demos, testing, and development**
- **Production environments** should not use this script

---

## 💡 Tips

1. **First Time Setup**: Run the script immediately after setting up MongoDB to have data ready for testing
2. **Demo Preparation**: Reseed data before demos to ensure fresh, consistent amounts
3. **Feature Testing**: Use the test user for all feature development to avoid polluting real user data
4. **Performance Testing**: Modify transaction counts to test with larger datasets
5. **CI/CD Integration**: Include seeding in your test pipeline for consistent test data

---

**Last Updated**: 2025-12-15  
**Version**: 1.0.0  
**Maintainer**: FinSense AI Team
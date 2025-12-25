# 🧪 Plaid Custom Test Users Setup Guide

> **Quick Reference**: Create custom test users in Plaid Sandbox to simulate specific banking scenarios and test edge cases.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Accessing Custom Test Users](#accessing-custom-test-users)
- [Creating Custom Test Users](#creating-custom-test-users)
- [Pre-Built Test User Configurations](#pre-built-test-user-configurations)
- [Testing Scenarios](#testing-scenarios)
- [Using Custom Test Users](#using-custom-test-users)
- [Best Practices](#best-practices)

---

## 🎯 Overview

Plaid Sandbox allows you to create up to **100 custom test users** with specific configurations to test various banking scenarios, account types, and edge cases.

### Why Use Custom Test Users?

- ✅ Test specific account balances and transaction histories
- ✅ Simulate different bank account types (checking, savings, credit cards)
- ✅ Test error scenarios (insufficient funds, locked accounts)
- ✅ Create reproducible test cases
- ✅ Test multi-account scenarios

---

## 🔑 Accessing Custom Test Users

### Step 1: Login to Plaid Dashboard

1. Go to [Plaid Dashboard](https://dashboard.plaid.com/)
2. Login with your credentials
3. Ensure you're in **Sandbox** environment (top-right corner)

### Step 2: Navigate to Test Users

1. Click on **Sandbox** in the left sidebar
2. Select **Test Users** tab
3. You'll see the custom test user creation interface

**Current Status**: You have created **0 out of 100** available custom users.

---

## ✨ Creating Custom Test Users

### Basic Configuration

#### 1. Username (Required)

```
Format: custom_<suffix>
Example: custom_restaurant_owner
         custom_high_balance
         custom_multi_account
```

**Rules**:
- Must start with `custom_`
- Use descriptive suffixes for easy identification
- Lowercase with underscores recommended

#### 2. Description (Optional)

Add a clear description of what this test user represents:

```
Examples:
- "Restaurant owner with high transaction volume"
- "User with multiple checking accounts"
- "Account with insufficient funds scenario"
- "Credit card with high balance"
```

#### 3. Configuration JSON (Required)

This is where you define the account structure, balances, and transactions.

---

## 📝 Pre-Built Test User Configurations

### Configuration 1: Basic Restaurant Owner

**Username**: `custom_restaurant_basic`  
**Description**: Restaurant owner with checking account and typical transactions

```json
{
  "override_accounts": [
    {
      "type": "depository",
      "subtype": "checking",
      "balances": {
        "available": 15000,
        "current": 15000
      },
      "transactions": {
        "days_requested": 90,
        "transactions": [
          {
            "amount": -250.00,
            "date": "2024-12-01",
            "name": "Daily Sales Deposit",
            "category": ["Transfer", "Deposit"]
          },
          {
            "amount": 450.00,
            "date": "2024-12-02",
            "name": "Sysco Food Supplies",
            "category": ["Food and Drink", "Groceries"]
          },
          {
            "amount": 2500.00,
            "date": "2024-12-05",
            "name": "Payroll - ADP",
            "category": ["Transfer", "Payroll"]
          }
        ]
      }
    }
  ]
}
```

### Configuration 2: Multi-Account Business

**Username**: `custom_multi_account`  
**Description**: Business with checking, savings, and credit card

```json
{
  "override_accounts": [
    {
      "type": "depository",
      "subtype": "checking",
      "balances": {
        "available": 25000,
        "current": 25000
      }
    },
    {
      "type": "depository",
      "subtype": "savings",
      "balances": {
        "available": 50000,
        "current": 50000
      }
    },
    {
      "type": "credit",
      "subtype": "credit card",
      "balances": {
        "available": 8000,
        "current": 2000,
        "limit": 10000
      }
    }
  ]
}
```

### Configuration 3: High Transaction Volume

**Username**: `custom_high_volume`  
**Description**: Account with many daily transactions (e-commerce business)

```json
{
  "override_accounts": [
    {
      "type": "depository",
      "subtype": "checking",
      "balances": {
        "available": 45000,
        "current": 45000
      },
      "transactions": {
        "days_requested": 30,
        "transactions": [
          {
            "amount": -150.00,
            "date": "2024-12-14",
            "name": "Stripe Payment",
            "category": ["Transfer", "Deposit"]
          },
          {
            "amount": -200.00,
            "date": "2024-12-14",
            "name": "Square Payment",
            "category": ["Transfer", "Deposit"]
          },
          {
            "amount": -175.00,
            "date": "2024-12-14",
            "name": "Online Order",
            "category": ["Transfer", "Deposit"]
          },
          {
            "amount": 500.00,
            "date": "2024-12-13",
            "name": "Facebook Ads",
            "category": ["Service", "Advertising"]
          },
          {
            "amount": 1200.00,
            "date": "2024-12-10",
            "name": "Inventory Purchase",
            "category": ["Shops", "Wholesale"]
          }
        ]
      }
    }
  ]
}
```

### Configuration 4: Low Balance / Insufficient Funds

**Username**: `custom_low_balance`  
**Description**: Account with low balance to test insufficient funds scenarios

```json
{
  "override_accounts": [
    {
      "type": "depository",
      "subtype": "checking",
      "balances": {
        "available": 150,
        "current": 150
      },
      "transactions": {
        "days_requested": 30,
        "transactions": [
          {
            "amount": 500.00,
            "date": "2024-12-10",
            "name": "Rent Payment",
            "category": ["Payment", "Rent"]
          },
          {
            "amount": -200.00,
            "date": "2024-12-12",
            "name": "Deposit",
            "category": ["Transfer", "Deposit"]
          }
        ]
      }
    }
  ]
}
```

### Configuration 5: New Business (Minimal History)

**Username**: `custom_new_business`  
**Description**: Newly opened business account with minimal transaction history

```json
{
  "override_accounts": [
    {
      "type": "depository",
      "subtype": "checking",
      "balances": {
        "available": 5000,
        "current": 5000
      },
      "transactions": {
        "days_requested": 7,
        "transactions": [
          {
            "amount": -5000.00,
            "date": "2024-12-08",
            "name": "Initial Deposit",
            "category": ["Transfer", "Deposit"]
          },
          {
            "amount": 150.00,
            "date": "2024-12-10",
            "name": "Office Supplies",
            "category": ["Shops", "Office Supplies"]
          }
        ]
      }
    }
  ]
}
```

### Configuration 6: Restaurant with Detailed Expenses

**Username**: `custom_restaurant_detailed`  
**Description**: Restaurant with realistic expense categories

```json
{
  "override_accounts": [
    {
      "type": "depository",
      "subtype": "checking",
      "balances": {
        "available": 18500,
        "current": 18500
      },
      "transactions": {
        "days_requested": 30,
        "transactions": [
          {
            "amount": -850.00,
            "date": "2024-12-14",
            "name": "Daily Sales",
            "category": ["Transfer", "Deposit"]
          },
          {
            "amount": 650.00,
            "date": "2024-12-13",
            "name": "Sysco Boston",
            "category": ["Food and Drink", "Groceries"]
          },
          {
            "amount": 3200.00,
            "date": "2024-12-12",
            "name": "Square Payroll",
            "category": ["Transfer", "Payroll"]
          },
          {
            "amount": 380.00,
            "date": "2024-12-11",
            "name": "Con Edison",
            "category": ["Service", "Utilities"]
          },
          {
            "amount": 250.00,
            "date": "2024-12-10",
            "name": "Facebook Ads",
            "category": ["Service", "Advertising"]
          },
          {
            "amount": 125.00,
            "date": "2024-12-09",
            "name": "Verizon Business",
            "category": ["Service", "Telecommunications"]
          }
        ]
      }
    }
  ]
}
```

---

## 🧪 Testing Scenarios

### Scenario 1: Test Account Connection Flow

1. Create `custom_test_connection` user with basic configuration
2. Use this user to test the Plaid Link flow
3. Verify account appears in your application

### Scenario 2: Test Transaction Sync

1. Create `custom_transaction_sync` with 50+ transactions
2. Connect the account
3. Verify all transactions sync correctly
4. Test transaction categorization

### Scenario 3: Test Multiple Accounts

1. Create `custom_multi_account` with 3+ accounts
2. Connect and verify all accounts appear
3. Test switching between accounts
4. Verify balance calculations

### Scenario 4: Test Edge Cases

1. Create `custom_edge_case` with:
   - Zero balance
   - Negative balance (overdraft)
   - Very high balance (>$1M)
   - No transactions
2. Test how your app handles these scenarios

---

## 🔧 Using Custom Test Users

### In Plaid Link Flow

When testing with Plaid Link in Sandbox mode:

1. **Select Institution**: Choose any test bank (e.g., "First Platypus Bank")
2. **Enter Credentials**:
   - **Username**: Your custom username (e.g., `custom_restaurant_basic`)
   - **Password**: `pass_good` (standard Plaid sandbox password)
3. **Complete Flow**: Your custom account configuration will be used

### Testing in FinSense AI

```bash
# 1. Ensure backend is running with Plaid credentials
cd backend
python -m uvicorn main:app --reload --port 8000

# 2. Start frontend
cd frontend
npm run dev

# 3. Login to FinSense AI
Email: test@example.com
Password: Test123!@#

# 4. Navigate to "Connect Accounts"
# 5. Click "Connect Bank Account"
# 6. In Plaid Link:
#    - Select any test bank
#    - Username: custom_restaurant_basic
#    - Password: pass_good
# 7. Complete connection
```

### Verifying Custom User Data

After connecting, verify:
- ✅ Account balance matches your configuration
- ✅ Transactions appear correctly
- ✅ Transaction dates are accurate
- ✅ Categories are properly assigned

---

## 💡 Best Practices

### Naming Conventions

```
custom_<business_type>_<scenario>

Examples:
✅ custom_restaurant_high_volume
✅ custom_retail_multi_account
✅ custom_service_low_balance
✅ custom_ecommerce_seasonal

❌ custom_test1
❌ custom_user
❌ custom_abc
```

### Organization Tips

1. **Group by Use Case**: Create users for specific features
   - `custom_dashboard_test` - For dashboard testing
   - `custom_reports_test` - For report generation
   - `custom_export_test` - For data export features

2. **Document Configurations**: Keep a local file with all your configurations

3. **Use Descriptive Descriptions**: Make it easy to remember what each user is for

4. **Version Control**: Save configurations in your project repository

```bash
# Create a directory for test user configs
mkdir -p backend/test_configs/plaid_users/

# Save each configuration
backend/test_configs/plaid_users/restaurant_basic.json
backend/test_configs/plaid_users/multi_account.json
backend/test_configs/plaid_users/high_volume.json
```

### Testing Workflow

1. **Create User** → Define configuration in Plaid Dashboard
2. **Document** → Save configuration to version control
3. **Test** → Use in your application
4. **Iterate** → Modify configuration as needed
5. **Share** → Team members can use same test users

---

## 🔍 Advanced Configuration Options

### Account Types

```json
{
  "type": "depository",  // or "credit", "loan", "investment"
  "subtype": "checking"  // or "savings", "credit card", "mortgage", etc.
}
```

### Balance Configuration

```json
{
  "balances": {
    "available": 10000,    // Available balance
    "current": 10000,      // Current balance
    "limit": 15000,        // Credit limit (for credit accounts)
    "iso_currency_code": "USD"
  }
}
```

### Transaction Configuration

```json
{
  "transactions": {
    "days_requested": 90,  // Number of days of history
    "transactions": [
      {
        "amount": -100.00,     // Negative = credit/deposit
        "date": "2024-12-01",  // YYYY-MM-DD format
        "name": "Vendor Name",
        "category": ["Category", "Subcategory"],
        "pending": false       // Optional: mark as pending
      }
    ]
  }
}
```

### Multiple Accounts Example

```json
{
  "override_accounts": [
    {
      "type": "depository",
      "subtype": "checking",
      "balances": {"available": 5000, "current": 5000}
    },
    {
      "type": "depository",
      "subtype": "savings",
      "balances": {"available": 20000, "current": 20000}
    },
    {
      "type": "credit",
      "subtype": "credit card",
      "balances": {
        "available": 8000,
        "current": 2000,
        "limit": 10000
      }
    }
  ]
}
```

---

## 📊 Recommended Test User Set

For comprehensive testing, create these 5 users:

| Username | Purpose | Key Features |
|----------|---------|--------------|
| `custom_basic_test` | General testing | Single checking account, moderate balance |
| `custom_multi_account` | Multi-account testing | Checking + Savings + Credit Card |
| `custom_high_volume` | Transaction volume testing | 100+ transactions |
| `custom_edge_case` | Edge case testing | Low balance, overdraft scenarios |
| `custom_restaurant` | Industry-specific | Realistic restaurant finances |

---

## 🐛 Troubleshooting

### Issue: Custom User Not Working

**Symptoms**: User not found or connection fails

**Solutions**:
1. Verify username starts with `custom_`
2. Check JSON configuration is valid (use JSON validator)
3. Ensure you're using `pass_good` as password
4. Verify you're in Sandbox environment

### Issue: Transactions Not Appearing

**Symptoms**: Account connects but no transactions show

**Solutions**:
1. Check `days_requested` is set correctly
2. Verify transaction dates are within requested range
3. Ensure transaction amounts are properly formatted (negative for deposits)
4. Check your app's transaction sync logic

### Issue: Invalid JSON Configuration

**Symptoms**: Error when creating user

**Solutions**:
1. Validate JSON syntax (use [JSONLint](https://jsonlint.com/))
2. Check all required fields are present
3. Ensure proper nesting of objects
4. Remove trailing commas

---

## 📚 Additional Resources

- [Plaid Sandbox Documentation](https://plaid.com/docs/sandbox/)
- [Plaid Custom Test Users Guide](https://plaid.com/docs/sandbox/custom-test-users/)
- [Plaid API Reference](https://plaid.com/docs/api/)
- [Transaction Categories](https://plaid.com/docs/api/products/transactions/#categoriesget)

---

## 🎯 Quick Start Checklist

- [ ] Login to Plaid Dashboard
- [ ] Navigate to Sandbox → Test Users
- [ ] Create `custom_restaurant_basic` user
- [ ] Copy configuration from this guide
- [ ] Save the user
- [ ] Test connection in your app
- [ ] Verify transactions sync correctly
- [ ] Create additional users for other scenarios

---

**Last Updated**: 2025-12-15  
**Version**: 1.0.0  
**Maintainer**: FinSense AI Team
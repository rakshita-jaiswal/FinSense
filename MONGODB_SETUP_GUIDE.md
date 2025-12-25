# MongoDB Setup & CRUD Guide for FinSense AI

This guide covers how to create, read, update, and delete data in MongoDB for testing purposes, both manually through MongoDB Atlas/Compass and programmatically through the application.

---

## Table of Contents
1. [Database Structure](#database-structure)
2. [Manual Setup via MongoDB Atlas/Compass](#manual-setup-via-mongodb-atlascompass)
3. [Programmatic Setup via Scripts](#programmatic-setup-via-scripts)
4. [CRUD Operations for Test Users](#crud-operations-for-test-users)
5. [Sample Data Management](#sample-data-management)
6. [Troubleshooting](#troubleshooting)

---

## Database Structure

### Collections:
- **users** - User accounts
- **subscriptions** - User subscription data
- **categories** - Transaction categories (shared across all users)
- **connected_accounts** - User's connected financial accounts
- **transactions** - Financial transactions
- **ai_conversations** - AI chat history

### Indexes:
- `users.email` - Unique index
- `subscriptions.user_id` - Unique index

---

## Manual Setup via MongoDB Atlas/Compass

### 1. Access MongoDB Atlas

1. Go to [MongoDB Atlas](https://cloud.mongodb.com/)
2. Log in to your account
3. Select your cluster
4. Click "Browse Collections"

### 2. Create Test User Manually

**Navigate to `users` collection and insert:**

```json
{
  "email": "testuser2@example.com",
  "password_hash": "$argon2id$v=19$m=65536,t=3,p=4$...",
  "first_name": "Test",
  "last_name": "User2",
  "business_name": "Test Business 2",
  "phone": null,
  "industry": null,
  "employees": null,
  "monthly_revenue": null,
  "created_at": {"$date": "2025-01-01T00:00:00.000Z"},
  "updated_at": {"$date": "2025-01-01T00:00:00.000Z"}
}
```

**Note**: You cannot manually create a valid password hash. Use the signup API endpoint or the `create_test_user.py` script instead.

### 3. Create Subscription for User

**Navigate to `subscriptions` collection and insert:**

```json
{
  "user_id": {"$oid": "USER_OBJECT_ID_HERE"},
  "is_trial_active": false,
  "trial_started_at": null,
  "trial_ends_at": null,
  "plan": "free",
  "created_at": {"$date": "2025-01-01T00:00:00.000Z"},
  "updated_at": {"$date": "2025-01-01T00:00:00.000Z"}
}
```

### 4. Create Connected Accounts

**Navigate to `connected_accounts` collection and insert:**

```json
{
  "user_id": {"$oid": "USER_OBJECT_ID_HERE"},
  "source": "square",
  "name": "Square POS",
  "connected_at": {"$date": "2025-01-01T00:00:00.000Z"}
}
```

### 5. View/Edit/Delete Data

**View Data:**
- Click on any collection to see documents
- Use the filter bar to search: `{"email": "test@example.com"}`

**Edit Data:**
- Click on a document
- Click "Edit Document"
- Modify fields
- Click "Update"

**Delete Data:**
- Click on a document
- Click "Delete Document"
- Confirm deletion

---

## Programmatic Setup via Scripts

### 1. Create Test User via Script

**Using the provided script:**

```bash
python create_test_user.py
```

This creates a user with:
- Email: test@example.com
- Password: password123

**Create additional test users:**

Edit `create_test_user.py` or create a new script:

```python
"""Create additional test users"""
import asyncio
import sys
import os
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.hash import argon2
from dotenv import load_dotenv
from datetime import datetime

load_dotenv(os.path.join(os.path.dirname(__file__), 'backend', '.env'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
from config import settings

async def create_user(email, password, first_name, last_name, business_name):
    """Create a test user"""
    client = AsyncIOMotorClient(settings.mongodb_uri)
    db = client[settings.database_name]
    
    # Check if user exists
    existing = await db.users.find_one({"email": email})
    if existing:
        print(f"[SKIP] User {email} already exists")
        client.close()
        return
    
    # Create user
    user_doc = {
        "email": email,
        "password_hash": argon2.hash(password),
        "first_name": first_name,
        "last_name": last_name,
        "business_name": business_name,
        "phone": None,
        "industry": None,
        "employees": None,
        "monthly_revenue": None,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = await db.users.insert_one(user_doc)
    user_id = result.inserted_id
    
    # Create subscription
    subscription_doc = {
        "user_id": user_id,
        "is_trial_active": False,
        "trial_started_at": None,
        "trial_ends_at": None,
        "plan": "free",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    await db.subscriptions.insert_one(subscription_doc)
    
    print(f"[OK] Created user: {email}")
    print(f"     Password: {password}")
    print(f"     User ID: {user_id}")
    
    client.close()

# Create multiple test users
async def main():
    users = [
        ("user1@example.com", "password123", "User", "One", "Business One"),
        ("user2@example.com", "password123", "User", "Two", "Business Two"),
        ("user3@example.com", "password123", "User", "Three", "Business Three"),
    ]
    
    for email, password, first, last, business in users:
        await create_user(email, password, first, last, business)

if __name__ == "__main__":
    asyncio.run(main())
```

### 2. Seed Sample Data

**Run the seed script:**

```bash
cd backend
python seed_data.py
```

This will:
- Seed 12 categories (if not already seeded)
- Seed connected accounts for test user
- Seed 80 sample transactions for test user

**Seed data for specific user:**

Create a custom seed script:

```python
"""Seed data for specific user"""
import asyncio
import sys
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), 'backend', '.env'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
from config import settings
from services.transaction_generator import generate_transactions_for_source

async def seed_user_data(user_email):
    """Seed accounts and transactions for specific user"""
    client = AsyncIOMotorClient(settings.mongodb_uri)
    db = client[settings.database_name]
    
    # Find user
    user = await db.users.find_one({"email": user_email})
    if not user:
        print(f"[ERROR] User {user_email} not found")
        client.close()
        return
    
    user_id = user["_id"]
    print(f"[OK] Found user: {user_email}")
    
    # Seed connected accounts
    accounts = [
        {"user_id": user_id, "source": "square", "name": "Square POS", "connected_at": datetime.utcnow()},
        {"user_id": user_id, "source": "stripe", "name": "Stripe Payments", "connected_at": datetime.utcnow()},
        {"user_id": user_id, "source": "bank", "name": "Bank Account", "connected_at": datetime.utcnow()},
    ]
    
    for account in accounts:
        existing = await db.connected_accounts.find_one({
            "user_id": user_id,
            "source": account["source"]
        })
        if not existing:
            await db.connected_accounts.insert_one(account)
            print(f"  [OK] Created {account['source']} account")
    
    # Seed transactions
    for source in ["square", "stripe", "bank"]:
        mock_trans = generate_transactions_for_source(source)
        trans_docs = []
        for trans in mock_trans:
            trans_docs.append({
                "user_id": user_id,
                "date": trans["date"],
                "vendor": trans["vendor"],
                "amount": trans["amount"],
                "category": trans["category"],
                "confidence": trans["confidence"],
                "status": trans["status"],
                "explanation": trans["explanation"],
                "payment_method": trans["payment_method"],
                "original_description": trans.get("original_description"),
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            })
        
        if trans_docs:
            await db.transactions.insert_many(trans_docs)
            print(f"  [OK] Created {len(trans_docs)} transactions from {source}")
    
    client.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python seed_user_data.py <user_email>")
        sys.exit(1)
    
    asyncio.run(seed_user_data(sys.argv[1]))
```

---

## CRUD Operations for Test Users

### Create (C)

**Via API (Recommended):**

```bash
curl -X POST http://localhost:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "password": "password123",
    "firstName": "New",
    "lastName": "User",
    "businessName": "New Business"
  }'
```

**Via Script:**
```bash
python create_test_user.py
```

### Read (R)

**Via MongoDB Atlas:**
1. Go to Browse Collections
2. Select `users` collection
3. Use filter: `{"email": "test@example.com"}`

**Via Python Script:**

```python
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv('backend/.env')
import sys
sys.path.insert(0, 'backend')
from config import settings

async def get_user(email):
    client = AsyncIOMotorClient(settings.mongodb_uri)
    db = client[settings.database_name]
    
    user = await db.users.find_one({"email": email})
    if user:
        print(f"User found: {user['first_name']} {user['last_name']}")
        print(f"Business: {user['business_name']}")
        print(f"User ID: {user['_id']}")
    else:
        print("User not found")
    
    client.close()

asyncio.run(get_user("test@example.com"))
```

### Update (U)

**Via API:**

```bash
# First login to get token
TOKEN=$(curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}' \
  | jq -r '.access_token')

# Update profile
curl -X PUT http://localhost:8000/api/v1/auth/profile \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "firstName": "Updated",
    "businessName": "Updated Business",
    "industry": "Restaurant",
    "employees": 10
  }'
```

**Via MongoDB Atlas:**
1. Find the user document
2. Click "Edit Document"
3. Modify fields
4. Click "Update"

### Delete (D)

**Via API:**

```bash
# Delete account (requires authentication)
curl -X DELETE http://localhost:8000/api/v1/auth/account \
  -H "Authorization: Bearer $TOKEN"
```

**Via Script:**

```bash
python delete_test_user.py
```

**Via MongoDB Atlas:**
1. Find the user document
2. Click "Delete Document"
3. Confirm deletion
4. **Important**: Also delete related data:
   - subscriptions (filter: `{"user_id": ObjectId("USER_ID")}`)
   - connected_accounts (filter: `{"user_id": ObjectId("USER_ID")}`)
   - transactions (filter: `{"user_id": ObjectId("USER_ID")}`)

---

## Sample Data Management

### View All Test Users

```python
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv('backend/.env')
import sys
sys.path.insert(0, 'backend')
from config import settings

async def list_users():
    client = AsyncIOMotorClient(settings.mongodb_uri)
    db = client[settings.database_name]
    
    users = await db.users.find({}).to_list(length=None)
    
    print(f"\nTotal users: {len(users)}\n")
    for user in users:
        print(f"Email: {user['email']}")
        print(f"Name: {user['first_name']} {user['last_name']}")
        print(f"Business: {user['business_name']}")
        print(f"ID: {user['_id']}")
        print("-" * 50)
    
    client.close()

asyncio.run(list_users())
```

### View User's Transactions

```python
async def view_user_transactions(email):
    client = AsyncIOMotorClient(settings.mongodb_uri)
    db = client[settings.database_name]
    
    user = await db.users.find_one({"email": email})
    if not user:
        print("User not found")
        client.close()
        return
    
    transactions = await db.transactions.find({"user_id": user["_id"]}).to_list(length=None)
    
    print(f"\nTransactions for {email}: {len(transactions)}\n")
    for trans in transactions[:10]:  # Show first 10
        print(f"{trans['date'].strftime('%Y-%m-%d')} | {trans['vendor']} | ${abs(trans['amount']):.2f} | {trans['category']}")
    
    client.close()

asyncio.run(view_user_transactions("test@example.com"))
```

### Clear All Test Data

```python
async def clear_test_data():
    """WARNING: This deletes ALL data for test users"""
    client = AsyncIOMotorClient(settings.mongodb_uri)
    db = client[settings.database_name]
    
    # Find all test users (emails containing 'test' or 'example')
    test_users = await db.users.find({
        "email": {"$regex": "test|example", "$options": "i"}
    }).to_list(length=None)
    
    for user in test_users:
        user_id = user["_id"]
        email = user["email"]
        
        # Delete user data
        await db.transactions.delete_many({"user_id": user_id})
        await db.connected_accounts.delete_many({"user_id": user_id})
        await db.subscriptions.delete_many({"user_id": user_id})
        await db.users.delete_one({"_id": user_id})
        
        print(f"[OK] Deleted all data for {email}")
    
    client.close()

# Uncomment to run (BE CAREFUL!)
# asyncio.run(clear_test_data())
```

---

## Troubleshooting

### Issue: Cannot connect to MongoDB

**Solution:**
1. Check `.env` file has correct `MONGODB_URI`
2. Verify MongoDB Atlas IP whitelist includes your IP
3. Test connection: `python -c "from pymongo import MongoClient; client = MongoClient('YOUR_URI'); print(client.server_info())"`

### Issue: Password hash doesn't work

**Solution:**
- Always use `argon2.hash()` from `passlib.hash` to create password hashes
- Never manually create password hashes
- Use the `create_test_user.py` script or signup API

### Issue: User has no transactions

**Solution:**
1. Check if connected accounts exist: `db.connected_accounts.find({"user_id": ObjectId("USER_ID")})`
2. Run seed script: `cd backend && python seed_data.py`
3. Or sync via API: `POST /api/v1/transactions/sync` with `{"source": "square"}`

### Issue: Duplicate key error on email

**Solution:**
- Email already exists in database
- Use different email or delete existing user first
- Check: `db.users.find({"email": "test@example.com"})`

---

## Quick Reference Commands

```bash
# Create test user
python create_test_user.py

# Seed all data
cd backend && python seed_data.py

# Delete test user
python delete_test_user.py

# Run comprehensive tests
python test_s5_comprehensive.py

# Start backend server
cd backend && python -m uvicorn main:app --reload --port 8000

# View MongoDB data
# Go to: https://cloud.mongodb.com/ → Browse Collections
```

---

## Test User Credentials

**Default Test User:**
- Email: test@example.com
- Password: password123
- Has 3 connected accounts (Square, Stripe, Bank)
- Has 80+ sample transactions

**Creating Additional Users:**
- Use signup API endpoint
- Or modify `create_test_user.py` script
- All users get free plan by default
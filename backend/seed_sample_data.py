"""
Standalone script to seed sample data into MongoDB for testing.
Run this script to populate the database with sample users, accounts, and transactions.

Usage:
    python seed_sample_data.py
"""
import asyncio
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import random
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DATABASE_NAME = "finsense"  # Database name from connection string


async def seed_sample_data():
    """Seed sample data into MongoDB."""
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[DATABASE_NAME]
    
    print("=" * 60)
    print("SEEDING SAMPLE DATA INTO MONGODB")
    print("=" * 60)
    
    # Create a test user (or use existing)
    test_email = "test@example.com"
    existing_user = await db.users.find_one({"email": test_email})
    
    if existing_user:
        user_id = existing_user["_id"]
        print(f"\n[OK] Using existing test user: {test_email}")
        print(f"  User ID: {user_id}")
    else:
        # Create test user
        from passlib.hash import argon2
        user_doc = {
            "email": test_email,
            "password_hash": argon2.hash("Test123!@#"),
            "first_name": "Test",
            "last_name": "User",
            "business_name": "Test Business LLC",
            "created_at": datetime.utcnow()
        }
        result = await db.users.insert_one(user_doc)
        user_id = result.inserted_id
        print(f"\n[OK] Created test user: {test_email}")
        print(f"  User ID: {user_id}")
        print(f"  Password: Test123!@#")
    
    # Check if user already has data
    existing_accounts = await db.connected_accounts.count_documents({"user_id": user_id})
    if existing_accounts > 0:
        print(f"\n[WARNING] User already has {existing_accounts} connected accounts")
        response = input("Delete existing data and reseed? (y/n): ")
        if response.lower() != 'y':
            print("Aborted.")
            return
        
        # Delete existing data
        await db.connected_accounts.delete_many({"user_id": user_id})
        await db.transactions.delete_many({"user_id": user_id})
        print("[OK] Deleted existing data")
    
    # 1. Create connected accounts
    print("\n" + "=" * 60)
    print("CREATING CONNECTED ACCOUNTS")
    print("=" * 60)
    
    accounts = [
        {
            "user_id": user_id,
            "source": "square",
            "name": "Square POS",
            "connected_at": datetime.utcnow() - timedelta(days=30)
        },
        {
            "user_id": user_id,
            "source": "stripe",
            "name": "Stripe Payments",
            "connected_at": datetime.utcnow() - timedelta(days=30)
        },
        {
            "user_id": user_id,
            "source": "bank",
            "name": "Chase Business Checking",
            "connected_at": datetime.utcnow() - timedelta(days=30)
        }
    ]
    
    await db.connected_accounts.insert_many(accounts)
    print(f"[OK] Created 3 connected accounts:")
    for acc in accounts:
        print(f"  - {acc['name']} ({acc['source']})")
    
    # 2. Generate sample transactions
    print("\n" + "=" * 60)
    print("GENERATING SAMPLE TRANSACTIONS")
    print("=" * 60)
    
    transactions = []
    now = datetime.utcnow()
    
    # Revenue transactions (40% of total)
    revenue_vendors = [
        "Daily Sales", "Online Orders", "Catering Service", "Gift Card Sales",
        "Delivery Orders", "Takeout Orders", "Event Booking", "Subscription Payment"
    ]
    
    print("\nGenerating revenue transactions...")
    for _ in range(30):
        days_ago = random.randint(0, 30)
        transaction_date = now - timedelta(days=days_ago, hours=random.randint(0, 23))
        
        transactions.append({
            "user_id": user_id,
            "date": transaction_date,
            "vendor": random.choice(revenue_vendors),
            "amount": -round(random.uniform(50, 800), 2),  # Negative for revenue
            "category": "Revenue",
            "confidence": random.uniform(0.92, 0.99),
            "status": "auto-approved",
            "explanation": "Categorized as Revenue based on payment processing pattern.",
            "payment_method": random.choice(["Square POS", "Stripe", "Bank Transfer"]),
            "original_description": None,
            "created_at": transaction_date,
            "updated_at": transaction_date
        })
    
    # Expense transactions (60% of total)
    expense_categories = [
        ("Sysco", "Inventory - Food & Supplies", 200, 800),
        ("US Foods", "Inventory - Food & Supplies", 180, 750),
        ("Restaurant Depot", "Inventory - Food & Supplies", 150, 600),
        ("Square Payroll", "Payroll", 2000, 4000),
        ("ADP Payroll", "Payroll", 1800, 3500),
        ("Con Edison", "Utilities", 200, 400),
        ("National Grid", "Utilities", 180, 350),
        ("Verizon Business", "Utilities", 100, 200),
        ("Facebook Ads", "Marketing", 100, 500),
        ("Google Ads", "Marketing", 150, 600),
        ("Amazon Business", "Office Supplies", 30, 250),
        ("Staples", "Office Supplies", 40, 180),
        ("State Farm Insurance", "Professional Fees", 200, 500),
        ("Equipment Repair Co", "Repairs & Maintenance", 100, 800),
    ]
    
    print("Generating expense transactions...")
    for _ in range(45):
        days_ago = random.randint(0, 30)
        transaction_date = now - timedelta(days=days_ago, hours=random.randint(0, 23))
        
        vendor, category, min_amt, max_amt = random.choice(expense_categories)
        amount = round(random.uniform(min_amt, max_amt), 2)
        confidence = random.uniform(0.75, 0.95)
        
        transactions.append({
            "user_id": user_id,
            "date": transaction_date,
            "vendor": vendor,
            "amount": amount,
            "category": category,
            "confidence": confidence,
            "status": "auto-approved" if confidence > 0.85 else "needs-review",
            "explanation": f"Categorized as {category} based on vendor pattern matching.",
            "payment_method": random.choice(["Business Debit", "Business Credit", "ACH Transfer", "Check"]),
            "original_description": vendor.upper(),
            "created_at": transaction_date,
            "updated_at": transaction_date
        })
    
    # Insert all transactions
    await db.transactions.insert_many(transactions)
    
    # Calculate summary stats
    revenue_count = sum(1 for t in transactions if t["amount"] < 0)
    expense_count = sum(1 for t in transactions if t["amount"] > 0)
    total_revenue = sum(abs(t["amount"]) for t in transactions if t["amount"] < 0)
    total_expenses = sum(t["amount"] for t in transactions if t["amount"] > 0)
    net_profit = total_revenue - total_expenses
    
    print(f"\n[OK] Created {len(transactions)} transactions")
    
    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"\nUser: {test_email}")
    print(f"User ID: {user_id}")
    print(f"\nConnected Accounts: 3")
    print(f"  - Square POS")
    print(f"  - Stripe Payments")
    print(f"  - Chase Business Checking")
    print(f"\nTransactions: {len(transactions)}")
    print(f"  - Revenue: {revenue_count} transactions (${total_revenue:,.2f})")
    print(f"  - Expenses: {expense_count} transactions (${total_expenses:,.2f})")
    print(f"  - Net Profit: ${net_profit:,.2f}")
    
    print("\n" + "=" * 60)
    print("SAMPLE DATA SEEDED SUCCESSFULLY!")
    print("=" * 60)
    print(f"\nYou can now login with:")
    print(f"  Email: {test_email}")
    print(f"  Password: Test123!@#")
    
    # Close connection
    client.close()


if __name__ == "__main__":
    asyncio.run(seed_sample_data())
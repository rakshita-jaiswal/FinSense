"""
Sample data seeder for new test users.
Automatically creates sample transactions and connected accounts for testing/demo purposes.
"""
from datetime import datetime, timedelta
from typing import List, Dict
from bson import ObjectId
import random


async def seed_sample_data_for_user(db, user_id: ObjectId):
    """
    Seed sample data for a new user including:
    - 3 connected accounts (Square, Stripe, Bank)
    - 50-80 sample transactions across last 30 days
    - Realistic financial data for dashboard testing
    """
    
    # Check if user already has data
    existing_accounts = await db.connected_accounts.count_documents({"user_id": user_id})
    if existing_accounts > 0:
        print(f"User {user_id} already has sample data, skipping...")
        return
    
    print(f"Seeding sample data for user {user_id}...")
    
    # 1. Create connected accounts
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
    print(f"  ✓ Created 3 connected accounts")
    
    # 2. Generate sample transactions
    transactions = []
    now = datetime.utcnow()
    
    # Revenue transactions (40% of total)
    revenue_vendors = [
        "Daily Sales", "Online Orders", "Catering Service", "Gift Card Sales",
        "Delivery Orders", "Takeout Orders", "Event Booking", "Subscription Payment"
    ]
    
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
    if transactions:
        await db.transactions.insert_many(transactions)
        print(f"  ✓ Created {len(transactions)} sample transactions")
    
    # Calculate summary stats
    revenue_count = sum(1 for t in transactions if t["amount"] < 0)
    expense_count = sum(1 for t in transactions if t["amount"] > 0)
    total_revenue = sum(abs(t["amount"]) for t in transactions if t["amount"] < 0)
    total_expenses = sum(t["amount"] for t in transactions if t["amount"] > 0)
    
    print(f"  ✓ Sample data summary:")
    print(f"    - Revenue transactions: {revenue_count} (${total_revenue:,.2f})")
    print(f"    - Expense transactions: {expense_count} (${total_expenses:,.2f})")
    print(f"    - Net profit: ${(total_revenue - total_expenses):,.2f}")
    
    return {
        "accounts_created": 3,
        "transactions_created": len(transactions),
        "revenue_count": revenue_count,
        "expense_count": expense_count,
        "total_revenue": total_revenue,
        "total_expenses": total_expenses
    }


async def seed_sample_data_on_signup(db, user_id: ObjectId):
    """
    Wrapper function to be called after user signup.
    Can be enabled/disabled based on environment.
    """
    try:
        result = await seed_sample_data_for_user(db, user_id)
        return result
    except Exception as e:
        print(f"Error seeding sample data for user {user_id}: {e}")
        return None
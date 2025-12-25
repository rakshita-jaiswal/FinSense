"""
Seed data script for FinSense AI
Seeds categories, connected accounts, and sample transactions for testing
"""
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from bson import ObjectId
from config import settings
from services.transaction_generator import generate_transactions_for_source
import asyncio


# Categories matching frontend mockData
CATEGORIES = [
    {
        "name": "Inventory - Food & Supplies",
        "type": "cogs",
        "color": "#3b82f6"
    },
    {
        "name": "Rent",
        "type": "expense",
        "color": "#8b5cf6"
    },
    {
        "name": "Utilities",
        "type": "expense",
        "color": "#06b6d4"
    },
    {
        "name": "Payroll",
        "type": "expense",
        "color": "#f59e0b"
    },
    {
        "name": "Loan Payments",
        "type": "expense",
        "color": "#dc2626"
    },
    {
        "name": "Marketing",
        "type": "expense",
        "color": "#ec4899"
    },
    {
        "name": "Office Supplies",
        "type": "expense",
        "color": "#10b981"
    },
    {
        "name": "Equipment",
        "type": "expense",
        "color": "#6366f1"
    },
    {
        "name": "Professional Fees",
        "type": "expense",
        "color": "#84cc16"
    },
    {
        "name": "Travel",
        "type": "expense",
        "color": "#f97316"
    },
    {
        "name": "Revenue",
        "type": "revenue",
        "color": "#22c55e"
    },
    {
        "name": "Repairs & Maintenance",
        "type": "expense",
        "color": "#ef4444"
    }
]


async def seed_categories():
    """Seed categories collection if empty"""
    client = AsyncIOMotorClient(settings.mongodb_uri)
    db = client[settings.database_name]
    categories_collection = db.categories
    
    # Check if categories already exist
    count = await categories_collection.count_documents({})
    
    if count == 0:
        print("Seeding categories...")
        result = await categories_collection.insert_many(CATEGORIES)
        print(f"[OK] Seeded {len(result.inserted_ids)} categories")
    else:
        print(f"[OK] Categories already seeded ({count} categories exist)")
    
    client.close()


async def seed_test_accounts_and_transactions():
    """Seed connected accounts and sample transactions for test user"""
    client = AsyncIOMotorClient(settings.mongodb_uri)
    db = client[settings.database_name]
    
    # Find test user
    test_user = await db.users.find_one({"email": "test@example.com"})
    
    if not test_user:
        print("[SKIP] Test user not found. Run create_test_user.py first.")
        client.close()
        return
    
    user_id = test_user["_id"]
    
    # Check if accounts already exist
    existing_accounts = await db.connected_accounts.count_documents({"user_id": user_id})
    
    if existing_accounts > 0:
        print(f"[OK] Test accounts already seeded ({existing_accounts} accounts exist)")
        
        # Check transactions
        existing_transactions = await db.transactions.count_documents({"user_id": user_id})
        print(f"[OK] Test transactions already seeded ({existing_transactions} transactions exist)")
        client.close()
        return
    
    # Seed connected accounts
    print("Seeding test connected accounts...")
    accounts_to_seed = [
        {
            "user_id": user_id,
            "source": "square",
            "name": "Square POS",
            "connected_at": datetime.utcnow()
        },
        {
            "user_id": user_id,
            "source": "stripe",
            "name": "Stripe Payments",
            "connected_at": datetime.utcnow()
        },
        {
            "user_id": user_id,
            "source": "bank",
            "name": "Bank Account - Chase Business",
            "connected_at": datetime.utcnow()
        }
    ]
    
    result = await db.connected_accounts.insert_many(accounts_to_seed)
    print(f"[OK] Seeded {len(result.inserted_ids)} connected accounts")
    
    # Seed sample transactions for each account
    print("Seeding sample transactions...")
    total_transactions = 0
    
    for source in ["square", "stripe", "bank"]:
        # Generate mock transactions
        mock_transactions = generate_transactions_for_source(source)
        
        # Prepare transactions for insertion
        transactions_to_insert = []
        for trans in mock_transactions:
            transaction_doc = {
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
            }
            transactions_to_insert.append(transaction_doc)
        
        # Insert transactions
        if transactions_to_insert:
            result = await db.transactions.insert_many(transactions_to_insert)
            count = len(result.inserted_ids)
            total_transactions += count
            print(f"  [OK] Seeded {count} transactions from {source}")
    
    print(f"[OK] Total {total_transactions} sample transactions seeded")
    client.close()


async def seed_all():
    """Seed all collections"""
    await seed_categories()
    await seed_test_accounts_and_transactions()


if __name__ == "__main__":
    asyncio.run(seed_all())
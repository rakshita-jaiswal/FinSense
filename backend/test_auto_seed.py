"""
Test script to verify automatic sample data seeding when a user connects their first account.
"""
import asyncio
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = "finsense"


async def test_auto_seed():
    """Test automatic sample data seeding on first account connection."""
    
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[DATABASE_NAME]
    
    print("=" * 60)
    print("TESTING AUTO-SEED ON FIRST ACCOUNT CONNECTION")
    print("=" * 60)
    
    # Create a test user
    test_email = f"autotest_{datetime.utcnow().timestamp()}@example.com"
    from passlib.hash import argon2
    
    user_doc = {
        "email": test_email,
        "password_hash": argon2.hash("Test123!@#"),
        "first_name": "Auto",
        "last_name": "Test",
        "business_name": "Auto Test Business",
        "created_at": datetime.utcnow()
    }
    
    result = await db.users.insert_one(user_doc)
    user_id = result.inserted_id
    
    print(f"\n[STEP 1] Created test user: {test_email}")
    print(f"  User ID: {user_id}")
    
    # Check initial state - should have no accounts or transactions
    account_count = await db.connected_accounts.count_documents({"user_id": user_id})
    transaction_count = await db.transactions.count_documents({"user_id": user_id})
    
    print(f"\n[STEP 2] Initial state:")
    print(f"  Connected accounts: {account_count}")
    print(f"  Transactions: {transaction_count}")
    
    if account_count > 0 or transaction_count > 0:
        print("\n[ERROR] User should start with no data!")
        return False
    
    # Simulate connecting first account (this should trigger auto-seed)
    print(f"\n[STEP 3] Simulating first account connection...")
    print("  This should automatically seed sample data...")
    
    # Import the seeder function
    from services.sample_data_seeder import seed_sample_data_for_user
    
    # Check if this is first account (it should be)
    is_first = account_count == 0
    print(f"  Is first account: {is_first}")
    
    if is_first:
        # Create the first account
        account_doc = {
            "user_id": user_id,
            "source": "square",
            "name": "Square POS",
            "connected_at": datetime.utcnow()
        }
        await db.connected_accounts.insert_one(account_doc)
        print("  [OK] Created first account: Square POS")
        
        # Trigger auto-seed
        try:
            await seed_sample_data_for_user(db, user_id)
            print("  [OK] Auto-seed completed successfully")
        except Exception as e:
            print(f"  [ERROR] Auto-seed failed: {e}")
            return False
    
    # Verify data was seeded
    print(f"\n[STEP 4] Verifying seeded data...")
    
    final_account_count = await db.connected_accounts.count_documents({"user_id": user_id})
    final_transaction_count = await db.transactions.count_documents({"user_id": user_id})
    
    print(f"  Connected accounts: {final_account_count}")
    print(f"  Transactions: {final_transaction_count}")
    
    # Should have 3 accounts (1 original + 2 from seeder) and 75 transactions
    expected_accounts = 3
    expected_transactions = 75
    
    success = True
    
    if final_account_count != expected_accounts:
        print(f"  [ERROR] Expected {expected_accounts} accounts, got {final_account_count}")
        success = False
    else:
        print(f"  [OK] Account count matches expected: {expected_accounts}")
    
    if final_transaction_count != expected_transactions:
        print(f"  [ERROR] Expected {expected_transactions} transactions, got {final_transaction_count}")
        success = False
    else:
        print(f"  [OK] Transaction count matches expected: {expected_transactions}")
    
    # Get sample of transactions
    transactions = await db.transactions.find({"user_id": user_id}).limit(5).to_list(length=5)
    
    print(f"\n[STEP 5] Sample transactions:")
    for i, txn in enumerate(transactions, 1):
        print(f"  {i}. {txn['vendor']}: ${abs(txn['amount']):.2f} - {txn['category']}")
    
    # Calculate totals
    revenue_pipeline = [
        {"$match": {"user_id": user_id, "amount": {"$lt": 0}}},
        {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
    ]
    expense_pipeline = [
        {"$match": {"user_id": user_id, "amount": {"$gt": 0}}},
        {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
    ]
    
    revenue_result = await db.transactions.aggregate(revenue_pipeline).to_list(length=1)
    expense_result = await db.transactions.aggregate(expense_pipeline).to_list(length=1)
    
    total_revenue = abs(revenue_result[0]["total"]) if revenue_result else 0
    total_expenses = expense_result[0]["total"] if expense_result else 0
    net_profit = total_revenue - total_expenses
    
    print(f"\n[STEP 6] Financial summary:")
    print(f"  Total Revenue: ${total_revenue:,.2f}")
    print(f"  Total Expenses: ${total_expenses:,.2f}")
    print(f"  Net Profit: ${net_profit:,.2f}")
    
    # Cleanup
    print(f"\n[CLEANUP] Removing test user and data...")
    await db.users.delete_one({"_id": user_id})
    await db.connected_accounts.delete_many({"user_id": user_id})
    await db.transactions.delete_many({"user_id": user_id})
    print("  [OK] Cleanup complete")
    
    # Final result
    print("\n" + "=" * 60)
    if success:
        print("TEST PASSED: Auto-seed works correctly!")
    else:
        print("TEST FAILED: Auto-seed did not work as expected")
    print("=" * 60)
    
    client.close()
    return success


if __name__ == "__main__":
    result = asyncio.run(test_auto_seed())
    sys.exit(0 if result else 1)
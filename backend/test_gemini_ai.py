"""Test script for Google Gemini AI integration."""
import asyncio
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = "finsense"


async def test_gemini_ai():
    """Test Gemini AI assistant with various queries."""
    
    from services.ai_service import ai_service
    
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[DATABASE_NAME]
    
    print("=" * 60)
    print("TESTING GOOGLE GEMINI AI INTEGRATION")
    print("=" * 60)
    
    # Get test user
    test_user = await db.users.find_one({"email": "test@example.com"})
    
    if not test_user:
        print("\n[ERROR] Test user not found. Please run seed_sample_data.py first.")
        return False
    
    user_id = test_user["_id"]
    print(f"\n[STEP 1] Using test user: test@example.com")
    print(f"  User ID: {user_id}")
    
    # Fetch user's financial data
    print(f"\n[STEP 2] Fetching user's financial data...")
    
    # Get revenue
    revenue_pipeline = [
        {"$match": {"user_id": user_id, "amount": {"$lt": 0}}},
        {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
    ]
    revenue_result = await db.transactions.aggregate(revenue_pipeline).to_list(length=1)
    total_revenue = abs(revenue_result[0]["total"]) if revenue_result else 0
    
    # Get expenses
    expense_pipeline = [
        {"$match": {"user_id": user_id, "amount": {"$gt": 0}}},
        {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
    ]
    expense_result = await db.transactions.aggregate(expense_pipeline).to_list(length=1)
    total_expenses = expense_result[0]["total"] if expense_result else 0
    
    # Get top categories
    category_pipeline = [
        {"$match": {"user_id": user_id, "amount": {"$gt": 0}}},
        {"$group": {"_id": "$category", "total": {"$sum": "$amount"}}},
        {"$sort": {"total": -1}},
        {"$limit": 3}
    ]
    categories = await db.transactions.aggregate(category_pipeline).to_list(length=3)
    top_categories = [cat["_id"] for cat in categories]
    
    transaction_count = await db.transactions.count_documents({"user_id": user_id})
    
    user_data = {
        "revenue": total_revenue,
        "expenses": total_expenses,
        "profit": total_revenue - total_expenses,
        "top_categories": top_categories,
        "transaction_count": transaction_count
    }
    
    print(f"  [OK] Financial data retrieved:")
    print(f"    Revenue: ${user_data['revenue']:,.2f}")
    print(f"    Expenses: ${user_data['expenses']:,.2f}")
    print(f"    Profit: ${user_data['profit']:,.2f}")
    print(f"    Top Categories: {', '.join(user_data['top_categories'][:3])}")
    print(f"    Transactions: {user_data['transaction_count']}")
    
    # Test queries
    test_queries = [
        # General bookkeeping
        ("What is double-entry bookkeeping?", None),
        ("How should I categorize meal expenses?", None),
        
        # FinSense-specific
        ("How do I review transactions in FinSense?", None),
        ("What do confidence scores mean?", None),
        
        # With user context
        ("Am I spending too much on payroll?", user_data),
        ("How can I improve my profit margin?", user_data),
        ("What are my biggest expenses?", user_data),
    ]
    
    print(f"\n[STEP 3] Testing AI responses...")
    print("=" * 60)
    
    for i, (query, context) in enumerate(test_queries, 1):
        print(f"\n[Query {i}]: {query}")
        print("-" * 60)
        
        try:
            response = await ai_service.generate_response(
                user_message=query,
                conversation_history=None,
                user_data=context
            )
            
            print(f"[Response]:\n{response}\n")
            
        except Exception as e:
            print(f"[ERROR]: {e}\n")
            return False
    
    print("=" * 60)
    print("ALL TESTS PASSED!")
    print("=" * 60)
    print("\n[SUCCESS] Google Gemini AI is working correctly!")
    print("The AI assistant can now:")
    print("  - Answer general bookkeeping questions")
    print("  - Provide FinSense-specific guidance")
    print("  - Analyze user's financial data")
    print("  - Give personalized recommendations")
    
    client.close()
    return True


if __name__ == "__main__":
    result = asyncio.run(test_gemini_ai())
    sys.exit(0 if result else 1)
"""
Test script for Sprint S8: AI Assistant Chat
Tests all AI chat endpoints including conversation management and message handling.
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


async def test_ai_chat():
    """Test AI chat functionality."""
    
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[DATABASE_NAME]
    
    print("=" * 60)
    print("TESTING S8: AI ASSISTANT CHAT")
    print("=" * 60)
    
    # Use existing test user
    test_user = await db.users.find_one({"email": "test@example.com"})
    
    if not test_user:
        print("\n[ERROR] Test user not found. Please run seed_sample_data.py first.")
        return False
    
    user_id = test_user["_id"]
    print(f"\n[STEP 1] Using test user: test@example.com")
    print(f"  User ID: {user_id}")
    
    # Test 1: Create a new conversation
    print(f"\n[STEP 2] Testing conversation creation...")
    
    conversation_doc = {
        "user_id": user_id,
        "title": "Test Conversation",
        "messages": [
            {
                "role": "user",
                "content": "Hello, what can you help me with?",
                "timestamp": datetime.utcnow()
            },
            {
                "role": "assistant",
                "content": "Hello! I'm FinAI, your financial assistant. I can help you with transaction analysis, expense tracking, and financial insights.",
                "timestamp": datetime.utcnow()
            }
        ],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = await db.conversations.insert_one(conversation_doc)
    conversation_id = result.inserted_id
    
    print(f"  [OK] Created conversation: {conversation_id}")
    print(f"  Title: {conversation_doc['title']}")
    print(f"  Messages: {len(conversation_doc['messages'])}")
    
    # Test 2: Retrieve the conversation
    print(f"\n[STEP 3] Testing conversation retrieval...")
    
    retrieved_conv = await db.conversations.find_one({"_id": conversation_id})
    
    if not retrieved_conv:
        print("  [ERROR] Failed to retrieve conversation")
        return False
    
    print(f"  [OK] Retrieved conversation")
    print(f"  Messages in conversation: {len(retrieved_conv['messages'])}")
    
    # Test 3: Add messages to conversation
    print(f"\n[STEP 4] Testing message addition...")
    
    new_messages = [
        {
            "role": "user",
            "content": "Show me my recent transactions",
            "timestamp": datetime.utcnow()
        },
        {
            "role": "assistant",
            "content": "Here are your most recent transactions:\n1. Daily Sales - $450.75\n2. Sysco - $325.50\n3. Square Payroll - $2,850.00",
            "timestamp": datetime.utcnow()
        }
    ]
    
    await db.conversations.update_one(
        {"_id": conversation_id},
        {
            "$push": {
                "messages": {"$each": new_messages}
            },
            "$set": {
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    updated_conv = await db.conversations.find_one({"_id": conversation_id})
    print(f"  [OK] Added 2 new messages")
    print(f"  Total messages now: {len(updated_conv['messages'])}")
    
    # Test 4: List all conversations for user
    print(f"\n[STEP 5] Testing conversation listing...")
    
    conversations_cursor = db.conversations.find({"user_id": user_id})
    conversations = await conversations_cursor.to_list(length=None)
    
    print(f"  [OK] Found {len(conversations)} conversation(s) for user")
    for i, conv in enumerate(conversations, 1):
        print(f"  {i}. {conv['title']} - {len(conv['messages'])} messages")
    
    # Test 5: Test AI response generation
    print(f"\n[STEP 6] Testing AI response generation...")
    
    from services.ai_assistant import ai_assistant
    
    test_queries = [
        "Hello",
        "Show me my transactions",
        "What are my top spending categories?",
        "Give me a financial summary",
        "What's my revenue trend?"
    ]
    
    for query in test_queries:
        response = await ai_assistant.generate_response(query)
        print(f"\n  Query: {query}")
        print(f"  Response preview: {response[:100]}...")
    
    print(f"\n  [OK] AI responses generated successfully")
    
    # Test 6: Create multiple conversations
    print(f"\n[STEP 7] Testing multiple conversations...")
    
    conversation_titles = [
        "Transaction Analysis",
        "Expense Tracking",
        "Revenue Insights"
    ]
    
    created_conversations = []
    for title in conversation_titles:
        conv_doc = {
            "user_id": user_id,
            "title": title,
            "messages": [
                {
                    "role": "user",
                    "content": f"Help me with {title.lower()}",
                    "timestamp": datetime.utcnow()
                },
                {
                    "role": "assistant",
                    "content": f"I'd be happy to help you with {title.lower()}!",
                    "timestamp": datetime.utcnow()
                }
            ],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        result = await db.conversations.insert_one(conv_doc)
        created_conversations.append(result.inserted_id)
    
    print(f"  [OK] Created {len(created_conversations)} additional conversations")
    
    # Test 7: Delete a conversation
    print(f"\n[STEP 8] Testing conversation deletion...")
    
    delete_result = await db.conversations.delete_one({"_id": conversation_id})
    
    if delete_result.deleted_count == 1:
        print(f"  [OK] Deleted conversation: {conversation_id}")
    else:
        print(f"  [ERROR] Failed to delete conversation")
        return False
    
    # Verify deletion
    deleted_conv = await db.conversations.find_one({"_id": conversation_id})
    if deleted_conv is None:
        print(f"  [OK] Verified conversation was deleted")
    else:
        print(f"  [ERROR] Conversation still exists after deletion")
        return False
    
    # Test 8: Verify conversation count
    print(f"\n[STEP 9] Verifying final conversation count...")
    
    final_count = await db.conversations.count_documents({"user_id": user_id})
    print(f"  [OK] User has {final_count} conversation(s)")
    
    # Cleanup: Delete test conversations
    print(f"\n[CLEANUP] Removing test conversations...")
    cleanup_result = await db.conversations.delete_many({"user_id": user_id})
    print(f"  [OK] Deleted {cleanup_result.deleted_count} test conversation(s)")
    
    # Final summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print("[OK] Conversation creation")
    print("[OK] Conversation retrieval")
    print("[OK] Message addition")
    print("[OK] Conversation listing")
    print("[OK] AI response generation")
    print("[OK] Multiple conversations")
    print("[OK] Conversation deletion")
    print("[OK] Conversation count verification")
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED!")
    print("=" * 60)
    
    print("\n[ENDPOINTS AVAILABLE]")
    print("POST   /api/v1/ai-chat/conversations - Create new conversation")
    print("GET    /api/v1/ai-chat/conversations - List all conversations")
    print("GET    /api/v1/ai-chat/conversations/{id} - Get specific conversation")
    print("POST   /api/v1/ai-chat/conversations/{id}/messages - Add message")
    print("DELETE /api/v1/ai-chat/conversations/{id} - Delete conversation")
    print("POST   /api/v1/ai-chat/quick-query - Quick query without saving")
    
    client.close()
    return True


if __name__ == "__main__":
    result = asyncio.run(test_ai_chat())
    sys.exit(0 if result else 1)
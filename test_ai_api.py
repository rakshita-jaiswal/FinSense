"""
Test AI Chat API endpoints with real authentication.
"""
import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

def test_ai_chat_api():
    """Test AI chat API endpoints."""
    
    print("=" * 60)
    print("TESTING AI CHAT API")
    print("=" * 60)
    
    # Step 1: Login to get JWT token
    print("\n[STEP 1] Logging in...")
    login_response = requests.post(
        f"{BASE_URL}/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "your-test-password-here"
        }
    )
    
    if login_response.status_code != 200:
        print(f"[ERROR] Login failed: {login_response.text}")
        return False
    
    token = login_response.json()["access_token"]
    print(f"[OK] Logged in successfully")
    print(f"  Token: {token[:50]}...")
    
    # Headers with authentication
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Step 2: Test quick query endpoint (no conversation saved)
    print("\n[STEP 2] Testing quick query endpoint...")
    quick_query_response = requests.post(
        f"{BASE_URL}/api/v1/ai-chat/quick-query",
        headers=headers,
        json={
            "message": "What is double-entry bookkeeping?"
        }
    )
    
    if quick_query_response.status_code == 200:
        response_data = quick_query_response.json()
        print(f"[OK] Quick query successful")
        print(f"  AI Response: {response_data['content'][:200]}...")
    else:
        print(f"[ERROR] Quick query failed: {quick_query_response.text}")
        return False
    
    # Step 3: Create a new conversation
    print("\n[STEP 3] Creating new conversation...")
    create_conv_response = requests.post(
        f"{BASE_URL}/api/v1/ai-chat/conversations",
        headers=headers,
        json={
            "initial_message": "Hello! Can you help me understand my business finances?"
        }
    )
    
    if create_conv_response.status_code == 201:
        conv_data = create_conv_response.json()
        conversation_id = conv_data["id"]
        print(f"[OK] Conversation created")
        print(f"  Conversation ID: {conversation_id}")
        print(f"  Title: {conv_data['title']}")
        print(f"  Messages: {len(conv_data['messages'])}")
        print(f"  AI Response: {conv_data['messages'][1]['content'][:200]}...")
    else:
        print(f"[ERROR] Create conversation failed: {create_conv_response.text}")
        return False
    
    # Step 4: Add message to conversation
    print("\n[STEP 4] Adding message to conversation...")
    add_message_response = requests.post(
        f"{BASE_URL}/api/v1/ai-chat/conversations/{conversation_id}/messages",
        headers=headers,
        json={
            "message": "What are my biggest expenses?"
        }
    )
    
    if add_message_response.status_code == 200:
        message_data = add_message_response.json()
        print(f"[OK] Message added successfully")
        print(f"  AI Response: {message_data['content'][:200]}...")
    else:
        print(f"[ERROR] Add message failed: {add_message_response.text}")
        return False
    
    # Step 5: Get conversation with full history
    print("\n[STEP 5] Retrieving conversation...")
    get_conv_response = requests.get(
        f"{BASE_URL}/api/v1/ai-chat/conversations/{conversation_id}",
        headers=headers
    )
    
    if get_conv_response.status_code == 200:
        conv_data = get_conv_response.json()
        print(f"[OK] Conversation retrieved")
        print(f"  Total messages: {len(conv_data['messages'])}")
        for i, msg in enumerate(conv_data['messages'], 1):
            print(f"  Message {i} ({msg['role']}): {msg['content'][:100]}...")
    else:
        print(f"[ERROR] Get conversation failed: {get_conv_response.text}")
        return False
    
    # Step 6: List all conversations
    print("\n[STEP 6] Listing all conversations...")
    list_conv_response = requests.get(
        f"{BASE_URL}/api/v1/ai-chat/conversations",
        headers=headers
    )
    
    if list_conv_response.status_code == 200:
        conversations = list_conv_response.json()["conversations"]
        print(f"[OK] Found {len(conversations)} conversation(s)")
        for conv in conversations:
            print(f"  - {conv['title']} ({conv['message_count']} messages)")
    else:
        print(f"[ERROR] List conversations failed: {list_conv_response.text}")
        return False
    
    # Step 7: Test with financial context
    print("\n[STEP 7] Testing with financial context...")
    context_query_response = requests.post(
        f"{BASE_URL}/api/v1/ai-chat/quick-query",
        headers=headers,
        json={
            "message": "Am I spending too much on payroll? Give me specific advice."
        }
    )
    
    if context_query_response.status_code == 200:
        response_data = context_query_response.json()
        print(f"[OK] Context-aware query successful")
        print(f"  AI Response: {response_data['content'][:300]}...")
    else:
        print(f"[ERROR] Context query failed: {context_query_response.text}")
        return False
    
    # Step 8: Delete conversation
    print("\n[STEP 8] Deleting conversation...")
    delete_response = requests.delete(
        f"{BASE_URL}/api/v1/ai-chat/conversations/{conversation_id}",
        headers=headers
    )
    
    if delete_response.status_code == 200:
        print(f"[OK] Conversation deleted successfully")
    else:
        print(f"[ERROR] Delete conversation failed: {delete_response.text}")
        return False
    
    print("\n" + "=" * 60)
    print("ALL API TESTS PASSED!")
    print("=" * 60)
    print("\n[SUMMARY]")
    print("[OK] Quick query endpoint working")
    print("[OK] Create conversation working")
    print("[OK] Add message to conversation working")
    print("[OK] Get conversation working")
    print("[OK] List conversations working")
    print("[OK] Context-aware responses working")
    print("[OK] Delete conversation working")
    print("\n[NEXT STEPS]")
    print("1. Open frontend: http://localhost:5173")
    print("2. Login with: test@example.com / your-test-password")
    print("3. Navigate to AI Assistant page")
    print("4. Test the chat interface")
    
    return True


if __name__ == "__main__":
    try:
        success = test_ai_chat_api()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n[ERROR] Test failed with exception: {e}")
        exit(1)
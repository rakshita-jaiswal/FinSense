"""
Test script for S5: Account Connection & Transaction Sync
Tests:
1. Connect account endpoint
2. Get connected accounts endpoint
3. Transaction sync endpoint
4. Get transactions endpoint
5. Disconnect account endpoint
"""
import asyncio
import sys
import os
import httpx
from dotenv import load_dotenv

# Load environment variables from backend/.env
load_dotenv(os.path.join(os.path.dirname(__file__), 'backend', '.env'))

# Add backend to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
from backend.config import settings

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')


async def get_auth_token():
    """Login and get authentication token."""
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        login_response = await client.post(
            f"{base_url}/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "password123"
            }
        )
        
        if login_response.status_code != 200:
            print("[FAIL] Login failed")
            print(f"  Response: {login_response.text}")
            return None
        
        return login_response.json()["access_token"]


async def test_connect_account(token: str):
    """Test connecting a Square account."""
    print("\n=== Test 1: Connect Account ===")
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{base_url}/api/v1/accounts/connect",
            json={
                "source": "square",
                "name": "Square POS"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code != 201:
            print(f"[FAIL] Connect account failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
        
        data = response.json()
        print(f"[OK] Connected account: {data['account']['name']} ({data['account']['source']})")
        return True


async def test_get_connected_accounts(token: str):
    """Test getting connected accounts."""
    print("\n=== Test 2: Get Connected Accounts ===")
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{base_url}/api/v1/accounts/connected",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code != 200:
            print(f"[FAIL] Get connected accounts failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False, None
        
        data = response.json()
        accounts = data.get("accounts", [])
        print(f"[OK] Found {len(accounts)} connected account(s)")
        
        for acc in accounts:
            print(f"  - {acc['name']} ({acc['source']})")
        
        return True, accounts[0]["id"] if accounts else None


async def test_sync_transactions(token: str):
    """Test syncing transactions from Square."""
    print("\n=== Test 3: Sync Transactions ===")
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{base_url}/api/v1/transactions/sync",
            json={"source": "square"},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code != 200:
            print(f"[FAIL] Sync transactions failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
        
        data = response.json()
        print(f"[OK] Synced {data['count']} transactions from {data['source']}")
        return True


async def test_get_transactions(token: str):
    """Test getting all transactions."""
    print("\n=== Test 4: Get Transactions ===")
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{base_url}/api/v1/transactions",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code != 200:
            print(f"[FAIL] Get transactions failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
        
        data = response.json()
        transactions = data.get("transactions", [])
        print(f"[OK] Retrieved {len(transactions)} transaction(s)")
        
        # Show first 5 transactions
        if transactions:
            print("\n  Sample transactions:")
            for trans in transactions[:5]:
                amount_str = f"${abs(trans['amount']):.2f}"
                trans_type = "Revenue" if trans['amount'] < 0 else "Expense"
                print(f"    - {trans['vendor']}: {amount_str} ({trans_type}) - {trans['category']}")
        
        return True


async def test_disconnect_account(token: str, account_id: str):
    """Test disconnecting an account."""
    print("\n=== Test 5: Disconnect Account ===")
    base_url = "http://localhost:8000"
    
    if not account_id:
        print("[SKIP] No account ID to disconnect")
        return True
    
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"{base_url}/api/v1/accounts/{account_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code != 200:
            print(f"[FAIL] Disconnect account failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
        
        print("[OK] Account disconnected successfully")
        return True


async def main():
    """Run all tests."""
    print("=" * 60)
    print("S5: Account Connection & Transaction Sync - Test Suite")
    print("=" * 60)
    
    # Get auth token
    token = await get_auth_token()
    if not token:
        print("\n[ERROR] Failed to authenticate")
        return 1
    
    print("[OK] Authentication successful")
    
    # Run tests
    test1_passed = await test_connect_account(token)
    test2_passed, account_id = await test_get_connected_accounts(token)
    test3_passed = await test_sync_transactions(token)
    test4_passed = await test_get_transactions(token)
    test5_passed = await test_disconnect_account(token, account_id)
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Connect Account: {'[PASSED]' if test1_passed else '[FAILED]'}")
    print(f"Get Connected Accounts: {'[PASSED]' if test2_passed else '[FAILED]'}")
    print(f"Sync Transactions: {'[PASSED]' if test3_passed else '[FAILED]'}")
    print(f"Get Transactions: {'[PASSED]' if test4_passed else '[FAILED]'}")
    print(f"Disconnect Account: {'[PASSED]' if test5_passed else '[FAILED]'}")
    
    all_passed = all([test1_passed, test2_passed, test3_passed, test4_passed, test5_passed])
    
    if all_passed:
        print("\n[SUCCESS] All S5 tests passed!")
        return 0
    else:
        print("\n[ERROR] Some tests failed")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
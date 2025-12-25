"""
Comprehensive test script for S5: Account Connection & Transaction Sync
Tests all three account types: Square, Stripe, and Bank
"""
import asyncio
import sys
import os
import httpx
from dotenv import load_dotenv

# Load environment variables from backend/.env
load_dotenv(os.path.join(os.path.dirname(__file__), 'backend', '.env'))

# Add backend to path for imports (if needed in future)
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
# from config import settings

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
            return None
        
        return login_response.json()["access_token"]


async def test_connect_all_accounts(token: str):
    """Test connecting all three account types."""
    print("\n=== Test 1: Connect All Account Types ===")
    base_url = "http://localhost:8000"
    
    accounts_to_connect = [
        {"source": "square", "name": "Square POS"},
        {"source": "stripe", "name": "Stripe Payments"},
        {"source": "bank", "name": "Bank Account - Chase Business"}
    ]
    
    connected_count = 0
    async with httpx.AsyncClient() as client:
        for account in accounts_to_connect:
            response = await client.post(
                f"{base_url}/api/v1/accounts/connect",
                json=account,
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code == 201:
                data = response.json()
                print(f"  [OK] Connected: {data['account']['name']} ({data['account']['source']})")
                connected_count += 1
            elif response.status_code == 400 and "already connected" in response.text:
                print(f"  [OK] Already connected: {account['name']} ({account['source']})")
                connected_count += 1
            else:
                print(f"  [FAIL] Failed to connect {account['name']}: {response.text}")
    
    return connected_count == 3


async def test_sync_all_accounts(token: str):
    """Test syncing transactions from all account types."""
    print("\n=== Test 2: Sync Transactions from All Accounts ===")
    base_url = "http://localhost:8000"
    
    sources = ["square", "stripe", "bank"]
    total_synced = 0
    
    async with httpx.AsyncClient() as client:
        for source in sources:
            response = await client.post(
                f"{base_url}/api/v1/transactions/sync",
                json={"source": source},
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code == 200:
                data = response.json()
                count = data['count']
                total_synced += count
                print(f"  [OK] Synced {count} transactions from {source}")
            else:
                print(f"  [FAIL] Failed to sync from {source}: {response.text}")
                return False
    
    print(f"\n  Total transactions synced: {total_synced}")
    return total_synced > 0


async def test_get_all_transactions(token: str):
    """Test getting all transactions."""
    print("\n=== Test 3: Get All Transactions ===")
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{base_url}/api/v1/transactions",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code != 200:
            print(f"[FAIL] Get transactions failed: {response.text}")
            return False
        
        data = response.json()
        transactions = data.get("transactions", [])
        print(f"[OK] Retrieved {len(transactions)} total transaction(s)")
        
        # Analyze transactions by source
        sources = {}
        revenue_count = 0
        expense_count = 0
        
        for trans in transactions:
            # Count by payment method (proxy for source)
            method = trans['payment_method']
            sources[method] = sources.get(method, 0) + 1
            
            # Count revenue vs expenses
            if trans['amount'] < 0:
                revenue_count += 1
            else:
                expense_count += 1
        
        print(f"\n  Transaction breakdown:")
        print(f"    Revenue transactions: {revenue_count}")
        print(f"    Expense transactions: {expense_count}")
        print(f"\n  By payment method:")
        for method, count in sources.items():
            print(f"    {method}: {count}")
        
        # Show sample transactions
        if transactions:
            print(f"\n  Sample transactions (first 10):")
            for trans in transactions[:10]:
                amount_str = f"${abs(trans['amount']):.2f}"
                trans_type = "Revenue" if trans['amount'] < 0 else "Expense"
                print(f"    - {trans['vendor']}: {amount_str} ({trans_type}) - {trans['category']}")
        
        return len(transactions) > 0


async def test_filter_transactions(token: str):
    """Test filtering transactions by status."""
    print("\n=== Test 4: Filter Transactions by Status ===")
    base_url = "http://localhost:8000"
    
    statuses = ["auto-approved", "needs-review"]
    
    async with httpx.AsyncClient() as client:
        for status in statuses:
            response = await client.get(
                f"{base_url}/api/v1/transactions?status={status}",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code == 200:
                data = response.json()
                count = len(data.get("transactions", []))
                print(f"  [OK] {status}: {count} transaction(s)")
            else:
                print(f"  [FAIL] Failed to filter by {status}")
                return False
    
    return True


async def test_search_transactions(token: str):
    """Test searching transactions."""
    print("\n=== Test 5: Search Transactions ===")
    base_url = "http://localhost:8000"
    
    search_terms = ["Revenue", "Sysco", "Payroll"]
    
    async with httpx.AsyncClient() as client:
        for term in search_terms:
            response = await client.get(
                f"{base_url}/api/v1/transactions?search={term}",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code == 200:
                data = response.json()
                count = len(data.get("transactions", []))
                print(f"  [OK] Search '{term}': {count} result(s)")
            else:
                print(f"  [FAIL] Failed to search for '{term}'")
                return False
    
    return True


async def main():
    """Run all tests."""
    print("=" * 70)
    print("S5: Comprehensive Account Connection & Transaction Sync Test Suite")
    print("=" * 70)
    
    # Get auth token
    token = await get_auth_token()
    if not token:
        print("\n[ERROR] Failed to authenticate")
        return 1
    
    print("[OK] Authentication successful")
    
    # Run tests
    test1_passed = await test_connect_all_accounts(token)
    test2_passed = await test_sync_all_accounts(token)
    test3_passed = await test_get_all_transactions(token)
    test4_passed = await test_filter_transactions(token)
    test5_passed = await test_search_transactions(token)
    
    # Summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    print(f"Connect All Accounts: {'[PASSED]' if test1_passed else '[FAILED]'}")
    print(f"Sync All Accounts: {'[PASSED]' if test2_passed else '[FAILED]'}")
    print(f"Get All Transactions: {'[PASSED]' if test3_passed else '[FAILED]'}")
    print(f"Filter Transactions: {'[PASSED]' if test4_passed else '[FAILED]'}")
    print(f"Search Transactions: {'[PASSED]' if test5_passed else '[FAILED]'}")
    
    all_passed = all([test1_passed, test2_passed, test3_passed, test4_passed, test5_passed])
    
    if all_passed:
        print("\n[SUCCESS] All comprehensive S5 tests passed!")
        return 0
    else:
        print("\n[ERROR] Some tests failed")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
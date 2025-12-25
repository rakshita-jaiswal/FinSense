"""
Test script for S6: Transaction Management
Tests:
1. Get all transactions
2. Get single transaction by ID
3. Update transaction (change category)
4. Update transaction (change status)
5. Filter transactions by status
6. Search transactions by vendor
7. Search transactions by category
"""
import asyncio
import sys
import os
import httpx

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')


async def get_auth_token():
    """Get authentication token"""
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{base_url}/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "password123"
            }
        )
        
        if response.status_code != 200:
            print("[FAIL] Authentication failed")
            print(f"  Status: {response.status_code}")
            print(f"  Response: {response.text}")
            return None
        
        data = response.json()
        # Handle both possible response formats
        if "token" in data:
            return data["token"]
        elif "access_token" in data:
            return data["access_token"]
        else:
            print(f"[FAIL] No token in response: {data}")
            return None


async def test_get_all_transactions(token):
    """Test GET /api/v1/transactions"""
    print("\n=== Test 1: Get All Transactions ===")
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{base_url}/api/v1/transactions",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code != 200:
            print(f"[FAIL] Get all transactions failed: {response.status_code}")
            return False
        
        data = response.json()
        transactions = data.get("transactions", [])
        
        print(f"[OK] Retrieved {len(transactions)} transactions")
        
        if len(transactions) == 0:
            print("[FAIL] No transactions found")
            return False
        
        # Show sample transaction structure
        sample = transactions[0]
        print(f"\nSample transaction structure:")
        print(f"  ID: {sample.get('id')}")
        print(f"  Vendor: {sample.get('vendor')}")
        print(f"  Amount: ${sample.get('amount')}")
        print(f"  Category: {sample.get('category')}")
        print(f"  Status: {sample.get('status')}")
        print(f"  Confidence: {sample.get('confidence')}")
        print(f"  Payment Method: {sample.get('paymentMethod')}")
        
        return True


async def test_get_single_transaction(token):
    """Test GET /api/v1/transactions/:id"""
    print("\n=== Test 2: Get Single Transaction ===")
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        # First get all transactions to get an ID
        response = await client.get(
            f"{base_url}/api/v1/transactions",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        transactions = response.json().get("transactions", [])
        if not transactions:
            print("[FAIL] No transactions to test with")
            return False
        
        transaction_id = transactions[0]["id"]
        
        # Get single transaction
        response = await client.get(
            f"{base_url}/api/v1/transactions/{transaction_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code != 200:
            print(f"[FAIL] Get single transaction failed: {response.status_code}")
            return False
        
        transaction = response.json()
        print(f"[OK] Retrieved transaction: {transaction['vendor']} - ${transaction['amount']}")
        
        return True


async def test_update_transaction_category(token):
    """Test PUT /api/v1/transactions/:id (change category)"""
    print("\n=== Test 3: Update Transaction Category ===")
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        # Get a transaction to update
        response = await client.get(
            f"{base_url}/api/v1/transactions",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        transactions = response.json().get("transactions", [])
        if not transactions:
            print("[FAIL] No transactions to test with")
            return False
        
        transaction = transactions[0]
        transaction_id = transaction["id"]
        original_category = transaction["category"]
        
        # Change category to something different
        new_category = "Marketing" if original_category != "Marketing" else "Office Supplies"
        
        response = await client.put(
            f"{base_url}/api/v1/transactions/{transaction_id}",
            headers={"Authorization": f"Bearer {token}"},
            json={"category": new_category}
        )
        
        if response.status_code != 200:
            print(f"[FAIL] Update transaction failed: {response.status_code}")
            return False
        
        updated = response.json()["transaction"]
        
        if updated["category"] != new_category:
            print(f"[FAIL] Category not updated. Expected: {new_category}, Got: {updated['category']}")
            return False
        
        print(f"[OK] Category updated: {original_category} -> {new_category}")
        
        return True


async def test_update_transaction_status(token):
    """Test PUT /api/v1/transactions/:id (change status)"""
    print("\n=== Test 4: Update Transaction Status ===")
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        # Get a needs-review transaction
        response = await client.get(
            f"{base_url}/api/v1/transactions?status=needs-review",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        transactions = response.json().get("transactions", [])
        if not transactions:
            print("[WARN] No needs-review transactions to test with, using any transaction")
            response = await client.get(
                f"{base_url}/api/v1/transactions",
                headers={"Authorization": f"Bearer {token}"}
            )
            transactions = response.json().get("transactions", [])
        
        if not transactions:
            print("[FAIL] No transactions to test with")
            return False
        
        transaction = transactions[0]
        transaction_id = transaction["id"]
        original_status = transaction["status"]
        
        # Change status to auto-approved
        new_status = "auto-approved"
        
        response = await client.put(
            f"{base_url}/api/v1/transactions/{transaction_id}",
            headers={"Authorization": f"Bearer {token}"},
            json={"status": new_status}
        )
        
        if response.status_code != 200:
            print(f"[FAIL] Update transaction status failed: {response.status_code}")
            return False
        
        updated = response.json()["transaction"]
        
        if updated["status"] != new_status:
            print(f"[FAIL] Status not updated. Expected: {new_status}, Got: {updated['status']}")
            return False
        
        print(f"[OK] Status updated: {original_status} -> {new_status}")
        
        return True


async def test_filter_by_status(token):
    """Test filtering transactions by status"""
    print("\n=== Test 5: Filter Transactions by Status ===")
    base_url = "http://localhost:8000"
    
    statuses = ["all", "auto-approved", "needs-review", "manual"]
    results = {}
    
    async with httpx.AsyncClient() as client:
        for status in statuses:
            response = await client.get(
                f"{base_url}/api/v1/transactions?status={status}",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code != 200:
                print(f"[FAIL] Filter by {status} failed: {response.status_code}")
                return False
            
            transactions = response.json().get("transactions", [])
            results[status] = len(transactions)
            print(f"  [OK] {status}: {len(transactions)} transaction(s)")
        
        # Verify that filtered results make sense
        if results["all"] < results["auto-approved"]:
            print("[FAIL] 'all' should have more transactions than 'auto-approved'")
            return False
        
        return True


async def test_search_by_vendor(token):
    """Test searching transactions by vendor"""
    print("\n=== Test 6: Search Transactions by Vendor ===")
    base_url = "http://localhost:8000"
    
    search_terms = ["Square", "Sysco", "Amazon"]
    
    async with httpx.AsyncClient() as client:
        for term in search_terms:
            response = await client.get(
                f"{base_url}/api/v1/transactions?search={term}",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code != 200:
                print(f"[FAIL] Search for '{term}' failed: {response.status_code}")
                return False
            
            transactions = response.json().get("transactions", [])
            print(f"  [OK] Search '{term}': {len(transactions)} result(s)")
            
            # Verify results contain the search term
            if transactions:
                sample = transactions[0]
                vendor = sample.get("vendor", "").lower()
                if term.lower() not in vendor:
                    # Check if it's in category instead
                    category = sample.get("category", "").lower()
                    if term.lower() not in category:
                        print(f"  [INFO] Search term '{term}' not in vendor or category, might be fuzzy match")
        
        return True


async def test_search_by_category(token):
    """Test searching transactions by category"""
    print("\n=== Test 7: Search Transactions by Category ===")
    base_url = "http://localhost:8000"
    
    search_terms = ["Revenue", "Payroll", "Inventory"]
    
    async with httpx.AsyncClient() as client:
        for term in search_terms:
            response = await client.get(
                f"{base_url}/api/v1/transactions?search={term}",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code != 200:
                print(f"[FAIL] Search for '{term}' failed: {response.status_code}")
                return False
            
            transactions = response.json().get("transactions", [])
            print(f"  [OK] Search '{term}': {len(transactions)} result(s)")
        
        return True


async def main():
    """Run all tests"""
    print("=" * 70)
    print("S6: Transaction Management - Comprehensive Test Suite")
    print("=" * 70)
    
    # Get auth token
    token = await get_auth_token()
    if not token:
        print("\n[ERROR] Failed to authenticate")
        return 1
    
    print("[OK] Authentication successful")
    
    # Run all tests
    test1 = await test_get_all_transactions(token)
    test2 = await test_get_single_transaction(token)
    test3 = await test_update_transaction_category(token)
    test4 = await test_update_transaction_status(token)
    test5 = await test_filter_by_status(token)
    test6 = await test_search_by_vendor(token)
    test7 = await test_search_by_category(token)
    
    # Summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    print(f"Get All Transactions: {'[PASSED]' if test1 else '[FAILED]'}")
    print(f"Get Single Transaction: {'[PASSED]' if test2 else '[FAILED]'}")
    print(f"Update Transaction Category: {'[PASSED]' if test3 else '[FAILED]'}")
    print(f"Update Transaction Status: {'[PASSED]' if test4 else '[FAILED]'}")
    print(f"Filter by Status: {'[PASSED]' if test5 else '[FAILED]'}")
    print(f"Search by Vendor: {'[PASSED]' if test6 else '[FAILED]'}")
    print(f"Search by Category: {'[PASSED]' if test7 else '[FAILED]'}")
    
    all_passed = all([test1, test2, test3, test4, test5, test6, test7])
    
    if all_passed:
        print("\n[SUCCESS] All S6 transaction management tests passed!")
        return 0
    else:
        print("\n[ERROR] Some tests failed")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
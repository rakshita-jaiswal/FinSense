"""
Test script for S7: Dashboard Analytics
Tests all dashboard endpoints:
1. GET /api/v1/dashboard/stats
2. GET /api/v1/dashboard/revenue-trend
3. GET /api/v1/dashboard/expense-breakdown
4. GET /api/v1/dashboard/recent-transactions
5. GET /api/v1/dashboard/alerts
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
        if "token" in data:
            return data["token"]
        elif "access_token" in data:
            return data["access_token"]
        else:
            print(f"[FAIL] No token in response: {data}")
            return None


async def test_dashboard_stats(token):
    """Test GET /api/v1/dashboard/stats"""
    print("\n=== Test 1: Dashboard Stats ===")
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{base_url}/api/v1/dashboard/stats",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code != 200:
            print(f"[FAIL] Stats endpoint failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
        
        data = response.json()
        
        # Check required fields
        required_fields = [
            "monthlyRevenue", "netProfit", "totalExpenses", "cashBalance",
            "revenueChange", "profitChange", "expensesChange", "cashChange"
        ]
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            print(f"[FAIL] Missing fields: {missing_fields}")
            return False
        
        print(f"[OK] Dashboard stats retrieved successfully")
        print(f"  Monthly Revenue: ${data['monthlyRevenue']:,.2f}")
        print(f"  Net Profit: ${data['netProfit']:,.2f}")
        print(f"  Total Expenses: ${data['totalExpenses']:,.2f}")
        print(f"  Cash Balance: ${data['cashBalance']:,.2f}")
        print(f"  Revenue Change: {data['revenueChange']:+.1f}%")
        print(f"  Profit Change: {data['profitChange']:+.1f}%")
        
        return True


async def test_revenue_trend(token):
    """Test GET /api/v1/dashboard/revenue-trend"""
    print("\n=== Test 2: Revenue Trend ===")
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{base_url}/api/v1/dashboard/revenue-trend",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code != 200:
            print(f"[FAIL] Revenue trend endpoint failed: {response.status_code}")
            return False
        
        data = response.json()
        
        if "data" not in data:
            print("[FAIL] Missing 'data' field")
            return False
        
        trend_data = data["data"]
        
        if len(trend_data) != 7:
            print(f"[FAIL] Expected 7 days of data, got {len(trend_data)}")
            return False
        
        print(f"[OK] Revenue trend retrieved successfully ({len(trend_data)} days)")
        print("\n  Last 7 days:")
        for day in trend_data:
            print(f"    {day['date']}: Revenue ${day['revenue']:,.2f}, Expenses ${day['expenses']:,.2f}")
        
        return True


async def test_expense_breakdown(token):
    """Test GET /api/v1/dashboard/expense-breakdown"""
    print("\n=== Test 3: Expense Breakdown ===")
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{base_url}/api/v1/dashboard/expense-breakdown",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code != 200:
            print(f"[FAIL] Expense breakdown endpoint failed: {response.status_code}")
            return False
        
        data = response.json()
        
        if "data" not in data:
            print("[FAIL] Missing 'data' field")
            return False
        
        breakdown = data["data"]
        
        print(f"[OK] Expense breakdown retrieved successfully ({len(breakdown)} categories)")
        
        if breakdown:
            print("\n  Top expense categories:")
            for i, cat in enumerate(breakdown[:5], 1):
                print(f"    {i}. {cat['category']}: ${cat['amount']:,.2f} ({cat['percentage']:.1f}%)")
        
        # Verify each category has required fields
        for cat in breakdown:
            required = ["category", "amount", "percentage", "color"]
            missing = [f for f in required if f not in cat]
            if missing:
                print(f"[FAIL] Category missing fields: {missing}")
                return False
        
        return True


async def test_recent_transactions(token):
    """Test GET /api/v1/dashboard/recent-transactions"""
    print("\n=== Test 4: Recent Transactions ===")
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{base_url}/api/v1/dashboard/recent-transactions",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code != 200:
            print(f"[FAIL] Recent transactions endpoint failed: {response.status_code}")
            return False
        
        data = response.json()
        
        if "transactions" not in data:
            print("[FAIL] Missing 'transactions' field")
            return False
        
        transactions = data["transactions"]
        
        if len(transactions) > 5:
            print(f"[FAIL] Expected max 5 transactions, got {len(transactions)}")
            return False
        
        print(f"[OK] Recent transactions retrieved successfully ({len(transactions)} transactions)")
        
        if transactions:
            print("\n  Most recent transactions:")
            for trans in transactions:
                amount_str = f"${abs(trans['amount']):,.2f}"
                trans_type = "Revenue" if trans['amount'] < 0 else "Expense"
                print(f"    • {trans['vendor']}: {amount_str} ({trans_type}) - {trans['category']}")
        
        return True


async def test_alerts(token):
    """Test GET /api/v1/dashboard/alerts"""
    print("\n=== Test 5: Financial Alerts ===")
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{base_url}/api/v1/dashboard/alerts",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code != 200:
            print(f"[FAIL] Alerts endpoint failed: {response.status_code}")
            return False
        
        data = response.json()
        
        if "alerts" not in data:
            print("[FAIL] Missing 'alerts' field")
            return False
        
        alerts = data["alerts"]
        
        print(f"[OK] Alerts retrieved successfully ({len(alerts)} alerts)")
        
        if alerts:
            print("\n  Active alerts:")
            for alert in alerts:
                icon = {"warning": "[!]", "info": "[i]", "success": "[OK]"}.get(alert['type'], "[*]")
                print(f"    {icon} [{alert['type'].upper()}] {alert['title']}")
                print(f"       {alert['message']}")
        else:
            print("  No active alerts")
        
        # Verify each alert has required fields
        for alert in alerts:
            required = ["id", "type", "title", "message", "date", "actionable"]
            missing = [f for f in required if f not in alert]
            if missing:
                print(f"[FAIL] Alert missing fields: {missing}")
                return False
        
        return True


async def main():
    """Run all tests"""
    print("=" * 70)
    print("S7: Dashboard Analytics - Comprehensive Test Suite")
    print("=" * 70)
    
    # Get auth token
    token = await get_auth_token()
    if not token:
        print("\n[ERROR] Failed to authenticate")
        return 1
    
    print("[OK] Authentication successful")
    
    # Run all tests
    test1 = await test_dashboard_stats(token)
    test2 = await test_revenue_trend(token)
    test3 = await test_expense_breakdown(token)
    test4 = await test_recent_transactions(token)
    test5 = await test_alerts(token)
    
    # Summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    print(f"Dashboard Stats: {'[PASSED]' if test1 else '[FAILED]'}")
    print(f"Revenue Trend: {'[PASSED]' if test2 else '[FAILED]'}")
    print(f"Expense Breakdown: {'[PASSED]' if test3 else '[FAILED]'}")
    print(f"Recent Transactions: {'[PASSED]' if test4 else '[FAILED]'}")
    print(f"Financial Alerts: {'[PASSED]' if test5 else '[FAILED]'}")
    
    all_passed = all([test1, test2, test3, test4, test5])
    
    if all_passed:
        print("\n[SUCCESS] All S7 dashboard analytics tests passed!")
        return 0
    else:
        print("\n[ERROR] Some tests failed")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
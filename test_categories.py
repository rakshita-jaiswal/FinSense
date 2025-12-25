"""
Test script for S4: Categories & Mock Data Seeding
Tests:
1. Categories collection is created
2. 12 categories are seeded
3. GET /api/v1/categories endpoint returns all categories
"""
import asyncio
import sys
import os
from motor.motor_asyncio import AsyncIOMotorClient
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


async def test_categories_seeded():
    """Test that categories are seeded in database"""
    print("\n=== Testing Categories Seeding ===")
    
    client = AsyncIOMotorClient(settings.mongodb_uri)
    db = client.finsense
    categories_collection = db.categories
    
    # Check if categories exist
    count = await categories_collection.count_documents({})
    print(f"[OK] Categories collection has {count} documents")
    
    if count != 12:
        print(f"[FAIL] Expected 12 categories, found {count}")
        client.close()
        return False
    
    # Fetch all categories
    categories = await categories_collection.find({}).to_list(length=None)
    
    print("\n=== Seeded Categories ===")
    for cat in categories:
        print(f"  • {cat['name']} ({cat['type']}) - {cat['color']}")
    
    client.close()
    return True


async def test_categories_endpoint():
    """Test GET /api/v1/categories endpoint"""
    print("\n=== Testing Categories Endpoint ===")
    
    base_url = "http://localhost:8000"
    
    # First, login to get token
    async with httpx.AsyncClient() as client:
        # Try to login with existing user
        login_response = await client.post(
            f"{base_url}/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "password123"
            }
        )
        
        if login_response.status_code != 200:
            print("[FAIL] Login failed. Please ensure you have a test user created.")
            print(f"  Status: {login_response.status_code}")
            print(f"  Response: {login_response.text}")
            return False
        
        token = login_response.json()["access_token"]
        print("[OK] Login successful")
        
        # Test categories endpoint
        categories_response = await client.get(
            f"{base_url}/api/v1/categories",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if categories_response.status_code != 200:
            print(f"[FAIL] Categories endpoint failed with status {categories_response.status_code}")
            print(f"  Response: {categories_response.text}")
            return False
        
        data = categories_response.json()
        categories = data.get("categories", [])
        
        print(f"[OK] Categories endpoint returned {len(categories)} categories")
        
        if len(categories) != 12:
            print(f"[FAIL] Expected 12 categories, got {len(categories)}")
            return False
        
        print("\n=== Categories from API ===")
        for cat in categories:
            print(f"  • {cat['name']} ({cat['type']}) - {cat['color']}")
        
        # Verify required categories exist
        required_categories = [
            "Inventory - Food & Supplies",
            "Rent",
            "Utilities",
            "Payroll",
            "Loan Payments",
            "Marketing",
            "Office Supplies",
            "Equipment",
            "Professional Fees",
            "Travel",
            "Revenue",
            "Repairs & Maintenance"
        ]
        
        category_names = [cat['name'] for cat in categories]
        missing = [name for name in required_categories if name not in category_names]
        
        if missing:
            print(f"\n[FAIL] Missing categories: {missing}")
            return False
        
        print("\n[OK] All required categories present")
        return True


async def main():
    """Run all tests"""
    print("=" * 60)
    print("S4: Categories & Mock Data Seeding - Test Suite")
    print("=" * 60)
    
    # Test 1: Check database seeding
    test1_passed = await test_categories_seeded()
    
    # Test 2: Check API endpoint
    test2_passed = await test_categories_endpoint()
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Database Seeding: {'[PASSED]' if test1_passed else '[FAILED]'}")
    print(f"API Endpoint: {'[PASSED]' if test2_passed else '[FAILED]'}")
    
    if test1_passed and test2_passed:
        print("\n[SUCCESS] All S4 tests passed!")
        return 0
    else:
        print("\n[ERROR] Some tests failed")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
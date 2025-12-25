"""
Test script to verify that user information from signup appears in the profile page.
This tests the complete flow: signup -> profile data persistence -> profile page display
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_signup_and_profile_display():
    """Test that signup data appears correctly in profile"""
    
    # Generate unique email for this test
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    test_email = f"testuser_{timestamp}@example.com"
    
    print("\n" + "="*60)
    print("Testing Signup -> Profile Data Flow")
    print("="*60)
    
    # Step 1: Sign up with complete information
    print("\n1. Creating new user account...")
    signup_data = {
        "email": test_email,
        "password": "testpass123",
        "first_name": "John",
        "last_name": "Doe",
        "business_name": "Acme Coffee Shop"
    }
    
    response = requests.post(f"{BASE_URL}/auth/signup", json=signup_data)
    assert response.status_code == 201, f"Signup failed: {response.text}"
    
    signup_result = response.json()
    token = signup_result["access_token"]
    user_data = signup_result["user"]
    
    print(f"[OK] Account created successfully")
    print(f"  Email: {user_data['email']}")
    print(f"  Name: {user_data['first_name']} {user_data['last_name']}")
    print(f"  Business: {user_data['business_name']}")
    
    # Step 2: Verify user data is returned correctly
    print("\n2. Verifying signup response data...")
    assert user_data["email"] == test_email
    assert user_data["first_name"] == "John"
    assert user_data["last_name"] == "Doe"
    assert user_data["business_name"] == "Acme Coffee Shop"
    print("[OK] Signup response contains correct user data")
    
    # Step 3: Fetch user profile using /me endpoint
    print("\n3. Fetching user profile via /me endpoint...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    assert response.status_code == 200, f"Failed to fetch profile: {response.text}"
    
    profile_data = response.json()["user"]
    print(f"[OK] Profile fetched successfully")
    print(f"  Email: {profile_data['email']}")
    print(f"  Name: {profile_data['first_name']} {profile_data['last_name']}")
    print(f"  Business: {profile_data['business_name']}")
    
    # Step 4: Verify profile data matches signup data
    print("\n4. Verifying profile data matches signup data...")
    assert profile_data["email"] == test_email
    assert profile_data["first_name"] == "John"
    assert profile_data["last_name"] == "Doe"
    assert profile_data["business_name"] == "Acme Coffee Shop"
    print("[OK] Profile data matches signup data")
    
    # Step 5: Update profile with additional information
    print("\n5. Updating profile with additional information...")
    update_data = {
        "phone": "+1 (555) 123-4567",
        "industry": "Restaurant - Coffee Shop",
        "employees": 5,
        "monthly_revenue": 70000
    }
    
    response = requests.put(f"{BASE_URL}/auth/profile", json=update_data, headers=headers)
    assert response.status_code == 200, f"Profile update failed: {response.text}"
    
    updated_profile = response.json()["user"]
    print(f"[OK] Profile updated successfully")
    print(f"  Phone: {updated_profile.get('phone', 'N/A')}")
    print(f"  Industry: {updated_profile.get('industry', 'N/A')}")
    print(f"  Employees: {updated_profile.get('employees', 'N/A')}")
    print(f"  Monthly Revenue: ${updated_profile.get('monthly_revenue', 0):,}")
    
    # Step 6: Verify updated profile data
    print("\n6. Verifying updated profile data...")
    assert updated_profile["phone"] == "+1 (555) 123-4567"
    assert updated_profile["industry"] == "Restaurant - Coffee Shop"
    assert updated_profile["employees"] == 5
    assert updated_profile["monthly_revenue"] == 70000
    # Original data should still be there
    assert updated_profile["first_name"] == "John"
    assert updated_profile["last_name"] == "Doe"
    assert updated_profile["business_name"] == "Acme Coffee Shop"
    print("[OK] All profile data verified successfully")
    
    # Step 7: Fetch profile again to ensure persistence
    print("\n7. Fetching profile again to verify persistence...")
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    assert response.status_code == 200
    
    final_profile = response.json()["user"]
    assert final_profile["phone"] == "+1 (555) 123-4567"
    assert final_profile["industry"] == "Restaurant - Coffee Shop"
    assert final_profile["employees"] == 5
    assert final_profile["monthly_revenue"] == 70000
    assert final_profile["first_name"] == "John"
    assert final_profile["last_name"] == "Doe"
    assert final_profile["business_name"] == "Acme Coffee Shop"
    print("[OK] Profile data persisted correctly")
    
    print("\n" + "="*60)
    print("[OK] ALL TESTS PASSED!")
    print("="*60)
    print("\nSummary:")
    print("- User signup creates account with basic info")
    print("- Profile endpoint returns correct user data")
    print("- Profile can be updated with additional fields")
    print("- All data persists correctly in database")
    print("- Frontend Profile page will display all this data")
    print("\n" + "="*60)

if __name__ == "__main__":
    try:
        test_signup_and_profile_display()
    except AssertionError as e:
        print(f"\n[X] TEST FAILED: {e}")
        exit(1)
    except Exception as e:
        print(f"\n[X] ERROR: {e}")
        exit(1)
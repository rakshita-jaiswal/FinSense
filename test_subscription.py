#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test script for subscription flow."""
import requests
import json
import sys
import io

# Fix encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_subscription_flow():
    print("=" * 60)
    print("Testing Subscription Flow")
    print("=" * 60)
    
    # Test 1: Sign up a new user
    print("\n1. Testing Signup (creates free plan subscription)...")
    signup_data = {
        "email": "testuser@example.com",
        "password": "test123456",
        "first_name": "Test",
        "last_name": "User",
        "business_name": "Test Business"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/signup", json=signup_data)
        if response.status_code == 201:
            data = response.json()
            token = data["token"]
            user_id = data["user"]["id"]
            print(f"✅ Signup successful!")
            print(f"   User ID: {user_id}")
            print(f"   Email: {data['user']['email']}")
            print(f"   Token: {token[:20]}...")
        else:
            print(f"❌ Signup failed: {response.status_code}")
            print(f"   Response: {response.text}")
            # Try to login instead if user exists
            print("\n   Trying to login with existing user...")
            login_response = requests.post(f"{BASE_URL}/auth/login", json={
                "email": signup_data["email"],
                "password": signup_data["password"]
            })
            if login_response.status_code == 200:
                data = login_response.json()
                token = data["token"]
                user_id = data["user"]["id"]
                print(f"✅ Login successful!")
                print(f"   User ID: {user_id}")
            else:
                print(f"❌ Login also failed: {login_response.status_code}")
                return
    except Exception as e:
        print(f"❌ Error during signup: {e}")
        return
    
    # Test 2: Check subscription status (should be free plan)
    print("\n2. Testing Get Subscription Status (should be free plan)...")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/subscription/status", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Subscription status retrieved!")
            print(f"   Plan: {data['plan']}")
            print(f"   Has Access: {data['hasAccess']}")
            print(f"   Trial Active: {data['isTrialActive']}")
            print(f"   Trial Ends At: {data['trialEndsAt']}")
        else:
            print(f"❌ Failed to get subscription status: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error getting subscription status: {e}")
    
    # Test 3: Start trial
    print("\n3. Testing Start Trial...")
    try:
        response = requests.post(f"{BASE_URL}/subscription/start-trial", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Trial started successfully!")
            print(f"   Message: {data['message']}")
            print(f"   Trial Ends At: {data['trialEndsAt']}")
        else:
            print(f"❌ Failed to start trial: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error starting trial: {e}")
    
    # Test 4: Check subscription status again (should show trial active)
    print("\n4. Testing Get Subscription Status (should show trial active)...")
    try:
        response = requests.get(f"{BASE_URL}/subscription/status", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Subscription status retrieved!")
            print(f"   Plan: {data['plan']}")
            print(f"   Has Access: {data['hasAccess']}")
            print(f"   Trial Active: {data['isTrialActive']}")
            print(f"   Trial Ends At: {data['trialEndsAt']}")
        else:
            print(f"❌ Failed to get subscription status: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error getting subscription status: {e}")
    
    # Test 5: Try to start trial again (should fail)
    print("\n5. Testing Start Trial Again (should fail - already used)...")
    try:
        response = requests.post(f"{BASE_URL}/subscription/start-trial", headers=headers)
        if response.status_code == 400:
            data = response.json()
            print(f"✅ Correctly rejected second trial attempt!")
            print(f"   Error: {data.get('detail', 'Unknown error')}")
        elif response.status_code == 200:
            print(f"❌ Trial started again (should have been rejected)")
        else:
            print(f"⚠️  Unexpected status code: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error testing second trial: {e}")
    
    print("\n" + "=" * 60)
    print("Subscription Flow Test Complete!")
    print("=" * 60)

if __name__ == "__main__":
    test_subscription_flow()
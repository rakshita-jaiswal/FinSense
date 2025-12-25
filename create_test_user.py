"""
Create a test user for testing purposes
"""
import asyncio
import sys
import os
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.hash import argon2
from dotenv import load_dotenv

# Load environment variables from backend/.env
load_dotenv(os.path.join(os.path.dirname(__file__), 'backend', '.env'))

# Add backend to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
from backend.config import settings


async def create_test_user():
    """Create a test user if it doesn't exist"""
    client = AsyncIOMotorClient(settings.mongodb_uri)
    db = client[settings.database_name]
    users_collection = db.users
    
    # Check if test user already exists
    existing_user = await users_collection.find_one({"email": "test@example.com"})
    
    if existing_user:
        print("[OK] Test user already exists")
    else:
        # Create test user
        from datetime import datetime
        
        test_user = {
            "email": "test@example.com",
            "password_hash": argon2.hash("password123"),
            "first_name": "Test",
            "last_name": "User",
            "business_name": "Test Business",
            "phone": None,
            "industry": None,
            "employees": None,
            "monthly_revenue": None,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = await users_collection.insert_one(test_user)
        print(f"[OK] Created test user with ID: {result.inserted_id}")
        print("     Email: test@example.com")
        print("     Password: password123")
    
    client.close()


if __name__ == "__main__":
    asyncio.run(create_test_user())
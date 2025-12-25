"""Create test user for AI testing."""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.hash import argon2
from datetime import datetime
import os
from dotenv import load_dotenv

# Load from backend/.env
load_dotenv("backend/.env")

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = "finsense"


async def create_test_user():
    """Create or update test user."""
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[DATABASE_NAME]
    
    email = "test@example.com"
    password = "Test123!@#"
    
    # Delete existing user
    await db.users.delete_one({"email": email})
    
    # Create new user with correct password
    user_doc = {
        "email": email,
        "password_hash": argon2.hash(password),
        "first_name": "Test",
        "last_name": "User",
        "business_name": "Test Business LLC",
        "created_at": datetime.utcnow()
    }
    
    result = await db.users.insert_one(user_doc)
    
    print(f"Created test user:")
    print(f"  Email: {email}")
    print(f"  Password: {password}")
    print(f"  User ID: {result.inserted_id}")
    
    client.close()


if __name__ == "__main__":
    asyncio.run(create_test_user())
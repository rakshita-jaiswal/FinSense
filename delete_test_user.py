"""Delete test user"""
import asyncio
import sys
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), 'backend', '.env'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
from backend.config import settings  # type: ignore

async def delete_user():
    client = AsyncIOMotorClient(settings.mongodb_uri)
    db = client[settings.database_name]
    await db.users.delete_one({'email': 'test@example.com'})
    print('Deleted test user')
    client.close()

asyncio.run(delete_user())
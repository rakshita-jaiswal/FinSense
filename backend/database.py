"""Database connection and utilities."""
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from config import settings


# Global MongoDB client (initialized in main.py lifespan)
mongodb_client: AsyncIOMotorClient = None


def get_database() -> AsyncIOMotorDatabase:
    """Get the MongoDB database instance."""
    return mongodb_client[settings.database_name]


async def init_db():
    """Initialize database indexes and collections."""
    db = get_database()
    
    # Create unique index on users.email
    await db.users.create_index("email", unique=True)
    
    # Create unique index on subscriptions.user_id
    await db.subscriptions.create_index("user_id", unique=True)
    
    print("Database indexes created successfully")
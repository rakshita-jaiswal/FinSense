from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from contextlib import asynccontextmanager

from config import settings
import database
from routers import auth, subscription, stripe, categories, accounts, transactions, dashboard, ai_chat
from seed_data import seed_all

# Use mock Plaid if credentials are not configured
if settings.plaid_client_id and settings.plaid_secret and settings.plaid_client_id != "your-plaid-client-id":
    from routers import plaid
else:
    from routers import plaid_mock as plaid
    print("WARNING: Using MOCK Plaid service (sample data) - Set real credentials in .env to use actual Plaid API")


# Global MongoDB client
mongodb_client: AsyncIOMotorClient = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events."""
    # Startup: Connect to MongoDB
    global mongodb_client
    mongodb_client = AsyncIOMotorClient(settings.mongodb_uri)
    database.mongodb_client = mongodb_client
    
    # Test the connection
    try:
        await mongodb_client.admin.command('ping')
        print("Successfully connected to MongoDB Atlas")
        
        # Initialize database indexes
        await database.init_db()
        
        # Seed initial data (categories)
        await seed_all()
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
    
    yield
    
    # Shutdown: Close MongoDB connection
    if mongodb_client:
        mongodb_client.close()
        print("MongoDB connection closed")


# Create FastAPI app
app = FastAPI(
    title="FinSense AI API",
    description="AI-powered financial management platform for small businesses",
    version="1.0.0",
    lifespan=lifespan
)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(auth.router)
app.include_router(subscription.router)
app.include_router(categories.router)
app.include_router(accounts.router)
app.include_router(transactions.router)
app.include_router(dashboard.router)
app.include_router(ai_chat.router)
app.include_router(plaid.router)  # Will be mock or real based on credentials
app.include_router(stripe.router)


@app.get("/healthz")
async def health_check():
    """Health check endpoint with database connection status."""
    db_status = "disconnected"
    
    try:
        # Ping the database
        await mongodb_client.admin.command('ping')
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "database": db_status,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "FinSense AI API",
        "version": "1.0.0",
        "docs": "/docs"
    } 

"""AI Chat routes for conversational financial assistant."""
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from bson import ObjectId
from typing import List, Dict

from models.conversation import (
    ConversationCreate,
    ConversationResponse,
    MessageCreate,
    MessageResponse,
    Message
)
from models.user import UserInDB
from auth.dependencies import get_current_user
from database import get_database
from services.sample_responses import get_sample_prompts
from services.ai_service import ai_service


router = APIRouter(prefix="/api/v1/ai-chat", tags=["ai-chat"])


async def fetch_user_financial_data(user_id: ObjectId, db) -> Dict:
    """Fetch user's financial data for AI context."""
    try:
        # Get revenue
        revenue_pipeline = [
            {"$match": {"user_id": user_id, "amount": {"$lt": 0}}},
            {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
        ]
        revenue_result = await db.transactions.aggregate(revenue_pipeline).to_list(length=1)
        total_revenue = abs(revenue_result[0]["total"]) if revenue_result else 0
        
        # Get expenses
        expense_pipeline = [
            {"$match": {"user_id": user_id, "amount": {"$gt": 0}}},
            {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
        ]
        expense_result = await db.transactions.aggregate(expense_pipeline).to_list(length=1)
        total_expenses = expense_result[0]["total"] if expense_result else 0
        
        # Get top categories
        category_pipeline = [
            {"$match": {"user_id": user_id, "amount": {"$gt": 0}}},
            {"$group": {"_id": "$category", "total": {"$sum": "$amount"}}},
            {"$sort": {"total": -1}},
            {"$limit": 3}
        ]
        categories = await db.transactions.aggregate(category_pipeline).to_list(length=3)
        top_categories = [cat["_id"] for cat in categories]
        
        # Get transaction count
        transaction_count = await db.transactions.count_documents({"user_id": user_id})
        
        return {
            "revenue": total_revenue,
            "expenses": total_expenses,
            "profit": total_revenue - total_expenses,
            "top_categories": top_categories,
            "transaction_count": transaction_count
        }
    except Exception as e:
        print(f"Error fetching user financial data: {e}")
        return {}


@router.post("/conversations", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
async def create_conversation(
    conversation_data: ConversationCreate,
    current_user: UserInDB = Depends(get_current_user)
):
    """
    Create a new AI conversation and get initial response.
    
    Creates a conversation with the user's first message and AI's response.
    """
    db = get_database()
    
    # Fetch user's financial data for context
    user_data = await fetch_user_financial_data(current_user.id, db)
    
    # Generate AI response to initial message
    ai_response = await ai_service.generate_response(
        user_message=conversation_data.initial_message,
        conversation_history=None,
        user_data=user_data
    )
    
    # Create conversation title from first message (truncated)
    title = conversation_data.title or conversation_data.initial_message[:50]
    if len(conversation_data.initial_message) > 50 and not conversation_data.title:
        title += "..."
    
    # Create conversation document
    now = datetime.utcnow()
    conversation_doc = {
        "user_id": current_user.id,
        "title": title,
        "messages": [
            {
                "role": "user",
                "content": conversation_data.initial_message,
                "timestamp": now
            },
            {
                "role": "assistant",
                "content": ai_response,
                "timestamp": now
            }
        ],
        "created_at": now,
        "updated_at": now
    }
    
    # Insert into database
    result = await db.conversations.insert_one(conversation_doc)
    conversation_id = str(result.inserted_id)
    
    # Return conversation with messages
    return ConversationResponse(
        id=conversation_id,
        user_id=str(current_user.id),
        title=title,
        messages=[
            Message(
                role="user",
                content=conversation_data.initial_message,
                timestamp=now
            ),
            Message(
                role="assistant",
                content=ai_response,
                timestamp=now
            )
        ],
        created_at=now,
        updated_at=now
    )


@router.get("/conversations", response_model=dict)
async def get_conversations(current_user: UserInDB = Depends(get_current_user)):
    """
    Get all conversations for the current user.
    
    Returns a list of conversations with basic info (no full message history).
    """
    db = get_database()
    
    # Fetch all conversations for user
    conversations_cursor = db.conversations.find(
        {"user_id": current_user.id}
    ).sort("updated_at", -1)  # Most recent first
    
    conversations = await conversations_cursor.to_list(length=None)
    
    # Convert to response format (without full messages)
    conversation_list = []
    for conv in conversations:
        # Get last message preview
        last_message = conv["messages"][-1] if conv["messages"] else None
        
        conversation_list.append({
            "id": str(conv["_id"]),
            "title": conv["title"],
            "last_message": last_message["content"][:100] if last_message else "",
            "message_count": len(conv["messages"]),
            "created_at": conv["created_at"].isoformat() + "Z",
            "updated_at": conv["updated_at"].isoformat() + "Z"
        })
    
    return {"conversations": conversation_list}


@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: str,
    current_user: UserInDB = Depends(get_current_user)
):
    """
    Get a specific conversation with full message history.
    """
    db = get_database()
    
    # Validate conversation_id
    if not ObjectId.is_valid(conversation_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid conversation ID"
        )
    
    # Find conversation
    conversation = await db.conversations.find_one({
        "_id": ObjectId(conversation_id),
        "user_id": current_user.id
    })
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    # Convert messages to Message objects
    messages = [
        Message(
            role=msg["role"],
            content=msg["content"],
            timestamp=msg["timestamp"]
        )
        for msg in conversation["messages"]
    ]
    
    return ConversationResponse(
        id=str(conversation["_id"]),
        user_id=str(conversation["user_id"]),
        title=conversation["title"],
        messages=messages,
        created_at=conversation["created_at"],
        updated_at=conversation["updated_at"]
    )


@router.post("/conversations/{conversation_id}/messages", response_model=MessageResponse)
async def add_message(
    conversation_id: str,
    message_data: MessageCreate,
    current_user: UserInDB = Depends(get_current_user)
):
    """
    Add a message to an existing conversation and get AI response.
    
    Appends user message and AI response to the conversation.
    """
    db = get_database()
    
    # Validate conversation_id
    if not ObjectId.is_valid(conversation_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid conversation ID"
        )
    
    # Find conversation
    conversation = await db.conversations.find_one({
        "_id": ObjectId(conversation_id),
        "user_id": current_user.id
    })
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    # Fetch user's financial data for context
    user_data = await fetch_user_financial_data(current_user.id, db)
    
    # Generate AI response with conversation history
    ai_response = await ai_service.generate_response(
        user_message=message_data.message,
        conversation_history=conversation.get("messages", []),
        user_data=user_data
    )
    
    # Create new messages
    now = datetime.utcnow()
    user_message = {
        "role": "user",
        "content": message_data.message,
        "timestamp": now
    }
    assistant_message = {
        "role": "assistant",
        "content": ai_response,
        "timestamp": now
    }
    
    # Update conversation with new messages
    await db.conversations.update_one(
        {"_id": ObjectId(conversation_id)},
        {
            "$push": {
                "messages": {
                    "$each": [user_message, assistant_message]
                }
            },
            "$set": {
                "updated_at": now
            }
        }
    )
    
    # Return AI response
    return MessageResponse(
        role="assistant",
        content=ai_response,
        timestamp=now
    )


@router.delete("/conversations/{conversation_id}", response_model=dict)
async def delete_conversation(
    conversation_id: str,
    current_user: UserInDB = Depends(get_current_user)
):
    """
    Delete a conversation.
    """
    db = get_database()
    
    # Validate conversation_id
    if not ObjectId.is_valid(conversation_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid conversation ID"
        )
    
    # Find and delete conversation
    result = await db.conversations.delete_one({
        "_id": ObjectId(conversation_id),
        "user_id": current_user.id
    })
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    return {"message": "Conversation deleted successfully"}


@router.post("/quick-query", response_model=MessageResponse)
async def quick_query(
    message_data: MessageCreate,
    current_user: UserInDB = Depends(get_current_user)
):
    """
    Send a quick query without creating a conversation.
    
    Useful for one-off questions that don't need to be saved.
    """
    db = get_database()
    
    # Fetch user's financial data for context
    user_data = await fetch_user_financial_data(current_user.id, db)
    
    # Generate AI response
    ai_response = await ai_service.generate_response(
        user_message=message_data.message,
        conversation_history=None,
        user_data=user_data
    )
    
    return MessageResponse(
        role="assistant",
        content=ai_response,
        timestamp=datetime.utcnow()
    )


@router.get("/sample-prompts", response_model=dict)
async def get_sample_prompts_endpoint():
    """
    Get sample prompts for the AI assistant.
    
    Returns a list of common questions users can ask.
    """
    prompts = get_sample_prompts()
    return {"prompts": prompts}


@router.get("/cache-stats", response_model=dict)
async def get_cache_stats(current_user: UserInDB = Depends(get_current_user)):
    """
    Get cache statistics (admin/debug endpoint).
    
    Returns cache hit rate and other statistics.
    """
    stats = ai_service.get_cache_stats()
    rate_limit_stats = await ai_service.get_rate_limit_status()
    
    return {
        "cache": stats,
        "rate_limit": rate_limit_stats
    }
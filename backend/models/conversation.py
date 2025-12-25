"""AI Conversation models for chat history."""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId


class Message(BaseModel):
    """Individual message in a conversation."""
    role: str = Field(..., description="Role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() + "Z"
        }


class ConversationCreate(BaseModel):
    """Request model for creating a new conversation."""
    title: Optional[str] = Field(None, description="Optional conversation title")
    initial_message: str = Field(..., description="First user message")


class ConversationResponse(BaseModel):
    """Response model for conversation."""
    id: str = Field(..., description="Conversation ID")
    user_id: str = Field(..., description="User ID")
    title: str = Field(..., description="Conversation title")
    messages: List[Message] = Field(default_factory=list, description="Conversation messages")
    created_at: datetime
    updated_at: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() + "Z"
        }


class MessageCreate(BaseModel):
    """Request model for adding a message to conversation."""
    message: str = Field(..., description="User message content")


class MessageResponse(BaseModel):
    """Response model for a single message."""
    role: str
    content: str
    timestamp: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() + "Z"
        }


class ConversationInDB(BaseModel):
    """Database model for conversation."""
    user_id: ObjectId
    title: str
    messages: List[dict]
    created_at: datetime
    updated_at: datetime
    
    model_config = {"arbitrary_types_allowed": True}
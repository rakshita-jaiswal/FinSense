"""Transaction model and schemas."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId


class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic v2."""
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import core_schema
        return core_schema.union_schema([
            core_schema.is_instance_schema(ObjectId),
            core_schema.no_info_plain_validator_function(cls.validate_str),
        ])
    
    @classmethod
    def validate_str(cls, v):
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str) and ObjectId.is_valid(v):
            return ObjectId(v)
        raise ValueError("Invalid ObjectId")
    
    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema, handler):
        return {"type": "string"}


class TransactionBase(BaseModel):
    """Base transaction schema."""
    date: datetime
    vendor: str = Field(..., min_length=1)
    amount: float
    category: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    status: str = Field(..., description="auto-approved, needs-review, or manual")
    explanation: str
    payment_method: str
    original_description: Optional[str] = None


class TransactionCreate(TransactionBase):
    """Schema for creating a new transaction."""
    pass


class TransactionInDB(TransactionBase):
    """Transaction schema as stored in database."""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class TransactionResponse(TransactionBase):
    """Transaction schema for API responses."""
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class TransactionUpdate(BaseModel):
    """Schema for updating a transaction."""
    category: Optional[str] = None
    status: Optional[str] = None
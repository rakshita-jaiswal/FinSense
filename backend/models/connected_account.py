"""Connected Account model and schemas."""
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


class ConnectedAccountBase(BaseModel):
    """Base connected account schema."""
    source: str = Field(..., description="Account source: square, stripe, or bank")
    name: str = Field(..., min_length=1, description="Account name")


class ConnectedAccountCreate(ConnectedAccountBase):
    """Schema for creating a new connected account."""
    pass


class ConnectedAccountInDB(ConnectedAccountBase):
    """Connected account schema as stored in database."""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    connected_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ConnectedAccountResponse(ConnectedAccountBase):
    """Connected account schema for API responses."""
    id: str
    connected_at: datetime
    
    class Config:
        from_attributes = True
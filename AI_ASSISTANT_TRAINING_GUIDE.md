# 🤖 AI Assistant Training Guide for FinSense AI

This comprehensive guide will help you integrate real AI/LLM capabilities into FinSense AI's chat assistant using free LLM APIs.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Free LLM API Options](#free-llm-api-options)
3. [Setup Instructions](#setup-instructions)
4. [Implementation Guide](#implementation-guide)
5. [Training & Fine-tuning](#training--fine-tuning)
6. [Bookkeeping Knowledge Base](#bookkeeping-knowledge-base)
7. [Testing & Optimization](#testing--optimization)

---

## 🎯 Overview

Currently, FinSense AI uses a **mock AI assistant** with pre-programmed responses. This guide will help you replace it with a **real AI model** that can:

- Answer general bookkeeping questions
- Provide FinSense-specific guidance
- Analyze user's financial data
- Give personalized recommendations
- Learn from conversations

---

## 🆓 Free LLM API Options

### Option 1: OpenAI GPT-3.5 Turbo (Recommended)
**Cost**: Free tier with $5 credit for new accounts
**Pros**: 
- High quality responses
- Fast inference
- Well-documented API
- Good for bookkeeping queries

**Cons**: 
- Requires credit card after free tier
- Rate limits on free tier

**Setup**:
```bash
pip install openai
```

**API Key**: Get from https://platform.openai.com/api-keys

---

### Option 2: Google Gemini (Free)
**Cost**: Completely free with generous limits
**Pros**:
- Truly free (no credit card required)
- 60 requests per minute
- Good reasoning capabilities
- Multimodal support

**Cons**:
- Slightly slower than GPT-3.5
- Newer, less community support

**Setup**:
```bash
pip install google-generativeai
```

**API Key**: Get from https://makersuite.google.com/app/apikey

---

### Option 3: Anthropic Claude (Limited Free)
**Cost**: Free tier available
**Pros**:
- Excellent for complex reasoning
- Strong at following instructions
- Good context window

**Cons**:
- Limited free tier
- Requires approval

**Setup**:
```bash
pip install anthropic
```

**API Key**: Get from https://console.anthropic.com/

---

### Option 4: Hugging Face Inference API (Free)
**Cost**: Free with rate limits
**Pros**:
- Access to many open-source models
- Completely free
- No credit card required

**Cons**:
- Slower inference
- Variable quality depending on model
- Rate limits

**Setup**:
```bash
pip install huggingface_hub
```

**API Key**: Get from https://huggingface.co/settings/tokens

---

### Option 5: Groq (Fast & Free)
**Cost**: Free with generous limits
**Pros**:
- **Extremely fast** (fastest inference)
- Free tier with good limits
- Supports Llama 3, Mixtral models

**Cons**:
- Newer service
- May have occasional downtime

**Setup**:
```bash
pip install groq
```

**API Key**: Get from https://console.groq.com/

---

## 🚀 Setup Instructions

### Step 1: Choose Your LLM Provider

For this guide, we'll use **Google Gemini** (completely free) and **Groq** (fast & free) as primary options.

### Step 2: Install Dependencies

```bash
cd backend
pip install google-generativeai groq openai
```

### Step 3: Add API Keys to `.env`

```env
# AI Assistant Configuration
AI_PROVIDER=gemini  # Options: gemini, groq, openai, anthropic, huggingface
GEMINI_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

### Step 4: Create AI Service Configuration

Create `backend/config/ai_config.py`:

```python
"""AI Assistant configuration."""
import os
from dotenv import load_dotenv

load_dotenv()

class AIConfig:
    """AI Assistant configuration."""
    
    # Provider selection
    PROVIDER = os.getenv("AI_PROVIDER", "gemini")  # gemini, groq, openai
    
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Model selection
    GEMINI_MODEL = "gemini-pro"
    GROQ_MODEL = "llama3-70b-8192"  # or "mixtral-8x7b-32768"
    OPENAI_MODEL = "gpt-3.5-turbo"
    
    # Generation parameters
    TEMPERATURE = 0.7  # 0.0 = deterministic, 1.0 = creative
    MAX_TOKENS = 1000
    TOP_P = 0.9
    
    # System prompt for bookkeeping context
    SYSTEM_PROMPT = """You are FinAI, an expert financial assistant for FinSense AI, 
a bookkeeping platform for small businesses. You help users with:

1. General bookkeeping questions and best practices
2. Understanding their financial data in FinSense
3. Transaction categorization and management
4. Financial analysis and insights
5. Tax preparation guidance
6. Cash flow management

Always provide clear, accurate, and actionable advice. When discussing FinSense features,
be specific about how to use them. For general bookkeeping questions, provide educational
responses with examples.

Keep responses concise but informative. Use bullet points for clarity when appropriate."""

ai_config = AIConfig()
```

---

## 💻 Implementation Guide

### Step 1: Create Real AI Service

Create `backend/services/ai_service.py`:

```python
"""Real AI service using LLM APIs."""
import os
from typing import Dict, Optional
import google.generativeai as genai
from groq import Groq
from openai import OpenAI

from config.ai_config import ai_config


class AIService:
    """AI service for generating intelligent responses."""
    
    def __init__(self):
        self.provider = ai_config.PROVIDER
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the appropriate AI client."""
        if self.provider == "gemini":
            genai.configure(api_key=ai_config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(ai_config.GEMINI_MODEL)
        
        elif self.provider == "groq":
            self.client = Groq(api_key=ai_config.GROQ_API_KEY)
        
        elif self.provider == "openai":
            self.client = OpenAI(api_key=ai_config.OPENAI_API_KEY)
    
    async def generate_response(
        self, 
        user_message: str, 
        conversation_history: list = None,
        user_data: Dict = None
    ) -> str:
        """
        Generate AI response using selected LLM provider.
        
        Args:
            user_message: User's question
            conversation_history: Previous messages for context
            user_data: User's financial data for personalized responses
        
        Returns:
            AI-generated response
        """
        # Build context from user data
        context = self._build_context(user_data)
        
        # Build full prompt
        full_prompt = self._build_prompt(user_message, context, conversation_history)
        
        # Generate response based on provider
        if self.provider == "gemini":
            return await self._generate_gemini(full_prompt)
        elif self.provider == "groq":
            return await self._generate_groq(full_prompt, conversation_history)
        elif self.provider == "openai":
            return await self._generate_openai(full_prompt, conversation_history)
        else:
            return "AI provider not configured. Please set AI_PROVIDER in .env"
    
    def _build_context(self, user_data: Dict = None) -> str:
        """Build context from user's financial data."""
        if not user_data:
            return ""
        
        context_parts = []
        
        if "revenue" in user_data:
            context_parts.append(f"Total Revenue: ${user_data['revenue']:,.2f}")
        
        if "expenses" in user_data:
            context_parts.append(f"Total Expenses: ${user_data['expenses']:,.2f}")
        
        if "profit" in user_data:
            context_parts.append(f"Net Profit: ${user_data['profit']:,.2f}")
        
        if "top_categories" in user_data:
            categories = ", ".join(user_data['top_categories'])
            context_parts.append(f"Top Expense Categories: {categories}")
        
        if "transaction_count" in user_data:
            context_parts.append(f"Total Transactions: {user_data['transaction_count']}")
        
        if context_parts:
            return "\n\nUser's Financial Context:\n" + "\n".join(context_parts)
        
        return ""
    
    def _build_prompt(
        self, 
        user_message: str, 
        context: str, 
        conversation_history: list = None
    ) -> str:
        """Build complete prompt with system instructions and context."""
        prompt_parts = [ai_config.SYSTEM_PROMPT]
        
        if context:
            prompt_parts.append(context)
        
        if conversation_history:
            prompt_parts.append("\n\nConversation History:")
            for msg in conversation_history[-5:]:  # Last 5 messages for context
                role = msg.get("role", "user")
                content = msg.get("content", "")
                prompt_parts.append(f"{role.capitalize()}: {content}")
        
        prompt_parts.append(f"\n\nUser Question: {user_message}")
        prompt_parts.append("\n\nAssistant Response:")
        
        return "\n".join(prompt_parts)
    
    async def _generate_gemini(self, prompt: str) -> str:
        """Generate response using Google Gemini."""
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=ai_config.TEMPERATURE,
                    max_output_tokens=ai_config.MAX_TOKENS,
                    top_p=ai_config.TOP_P,
                )
            )
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    async def _generate_groq(self, prompt: str, conversation_history: list = None) -> str:
        """Generate response using Groq."""
        try:
            messages = [
                {"role": "system", "content": ai_config.SYSTEM_PROMPT}
            ]
            
            if conversation_history:
                for msg in conversation_history[-5:]:
                    messages.append({
                        "role": msg.get("role", "user"),
                        "content": msg.get("content", "")
                    })
            
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=ai_config.GROQ_MODEL,
                messages=messages,
                temperature=ai_config.TEMPERATURE,
                max_tokens=ai_config.MAX_TOKENS,
                top_p=ai_config.TOP_P,
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    async def _generate_openai(self, prompt: str, conversation_history: list = None) -> str:
        """Generate response using OpenAI."""
        try:
            messages = [
                {"role": "system", "content": ai_config.SYSTEM_PROMPT}
            ]
            
            if conversation_history:
                for msg in conversation_history[-5:]:
                    messages.append({
                        "role": msg.get("role", "user"),
                        "content": msg.get("content", "")
                    })
            
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=ai_config.OPENAI_MODEL,
                messages=messages,
                temperature=ai_config.TEMPERATURE,
                max_tokens=ai_config.MAX_TOKENS,
                top_p=ai_config.TOP_P,
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"


# Singleton instance
ai_service = AIService()
```

### Step 2: Update AI Chat Router

Modify `backend/routers/ai_chat.py` to use the real AI service:

```python
# Replace this import:
# from services.ai_assistant import ai_assistant

# With this:
from services.ai_service import ai_service

# Then in your endpoints, replace:
# ai_response = await ai_assistant.generate_response(...)

# With:
ai_response = await ai_service.generate_response(
    user_message=message_data.message,
    conversation_history=conversation.get("messages", []),
    user_data=await fetch_user_financial_data(current_user.id, db)
)
```

### Step 3: Fetch User Financial Data

Add this helper function to `backend/routers/ai_chat.py`:

```python
async def fetch_user_financial_data(user_id: ObjectId, db) -> Dict:
    """Fetch user's financial data for AI context."""
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
```

---

## 📚 Training & Fine-tuning

### Bookkeeping Knowledge Base

Create a knowledge base file `backend/data/bookkeeping_knowledge.txt`:

```
# General Bookkeeping Concepts

## Double-Entry Bookkeeping
Every transaction affects at least two accounts. For every debit, there must be a corresponding credit.

## Chart of Accounts
A complete listing of every account in an accounting system:
- Assets (what you own)
- Liabilities (what you owe)
- Equity (owner's stake)
- Revenue (income)
- Expenses (costs)

## Accrual vs Cash Accounting
- Accrual: Record revenue when earned, expenses when incurred
- Cash: Record only when money changes hands

## Financial Statements
1. Balance Sheet: Assets = Liabilities + Equity
2. Income Statement: Revenue - Expenses = Net Income
3. Cash Flow Statement: Operating, Investing, Financing activities

## Common Expense Categories
- Cost of Goods Sold (COGS)
- Payroll and Benefits
- Rent and Utilities
- Marketing and Advertising
- Office Supplies
- Professional Fees
- Insurance
- Depreciation

## Tax Deductions for Small Business
- Business expenses (ordinary and necessary)
- Home office deduction
- Vehicle expenses
- Travel and meals (50% for meals)
- Equipment and supplies
- Professional development

## Best Practices
1. Reconcile accounts monthly
2. Keep personal and business finances separate
3. Save all receipts and documentation
4. Review financial statements regularly
5. Plan for quarterly tax payments
6. Maintain adequate cash reserves

# FinSense-Specific Features

## Transaction Management
- Automatic categorization with AI confidence scores
- Manual review for low-confidence transactions
- Bulk editing and filtering
- Search by vendor, amount, or date

## Dashboard Analytics
- Real-time financial statistics
- Revenue vs expense trends
- Category-wise expense breakdown
- Smart financial alerts

## Account Connections
- Square POS integration
- Stripe payment processing
- Bank account linking
- Automatic transaction sync

## AI Assistant Capabilities
- Answer bookkeeping questions
- Analyze financial data
- Provide personalized insights
- Suggest optimizations
```

### Enhanced System Prompt

Update `backend/config/ai_config.py` with enhanced prompt:

```python
SYSTEM_PROMPT = """You are FinAI, an expert financial assistant for FinSense AI.

CORE EXPERTISE:
- General bookkeeping principles and best practices
- Small business financial management
- Tax preparation and compliance
- Cash flow optimization
- Financial analysis and reporting

FINSENSE FEATURES YOU CAN HELP WITH:
1. Transaction Management: Categorization, review, bulk editing
2. Dashboard Analytics: Revenue trends, expense breakdowns, alerts
3. Account Connections: Square, Stripe, bank integrations
4. Financial Insights: Profit analysis, spending patterns, recommendations

RESPONSE GUIDELINES:
- Be conversational but professional
- Provide specific, actionable advice
- Use examples when helpful
- Reference FinSense features when relevant
- For general bookkeeping questions, educate the user
- For FinSense-specific questions, guide them through features
- Always consider the user's financial context when available

RESPONSE FORMAT:
- Start with a direct answer
- Provide supporting details
- Offer next steps or recommendations
- Keep responses concise (under 300 words unless complex topic)

Remember: You're helping small business owners manage their finances better."""
```

---

## 🧪 Testing & Optimization

### Test Script

Create `backend/test_real_ai.py`:

```python
"""Test real AI assistant responses."""
import asyncio
from services.ai_service import ai_service


async def test_ai_responses():
    """Test various bookkeeping queries."""
    
    test_queries = [
        # General bookkeeping
        "What is double-entry bookkeeping?",
        "How do I categorize a meal expense?",
        "What's the difference between accrual and cash accounting?",
        
        # FinSense-specific
        "How do I review transactions in FinSense?",
        "What do the confidence scores mean?",
        "How can I see my expense breakdown?",
        
        # With user context
        "Am I spending too much on payroll?",
        "How can I improve my profit margin?",
        "What are my biggest expenses?"
    ]
    
    # Mock user data
    user_data = {
        "revenue": 15234.56,
        "expenses": 11789.23,
        "profit": 3445.33,
        "top_categories": ["Payroll", "Inventory", "Utilities"],
        "transaction_count": 75
    }
    
    print("=" * 60)
    print("TESTING REAL AI ASSISTANT")
    print("=" * 60)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n[Query {i}]: {query}")
        print("-" * 60)
        
        response = await ai_service.generate_response(
            user_message=query,
            user_data=user_data if i > 6 else None
        )
        
        print(f"[Response]: {response}\n")


if __name__ == "__main__":
    asyncio.run(test_ai_responses())
```

Run the test:
```bash
cd backend
python test_real_ai.py
```

---

## 🎯 Best Practices

### 1. Rate Limiting
Implement rate limiting to avoid API quota issues:

```python
from functools import wraps
import time

def rate_limit(max_calls=10, time_window=60):
    """Rate limit decorator."""
    calls = []
    
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            now = time.time()
            calls[:] = [c for c in calls if c > now - time_window]
            
            if len(calls) >= max_calls:
                raise Exception("Rate limit exceeded")
            
            calls.append(now)
            return await func(*args, **kwargs)
        return wrapper
    return decorator
```

### 2. Caching Common Responses
Cache frequently asked questions:

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_response(query: str) -> str:
    """Cache common bookkeeping questions."""
    common_qa = {
        "what is bookkeeping": "Bookkeeping is the process of recording...",
        "how to categorize expenses": "Expenses should be categorized based on..."
    }
    return common_qa.get(query.lower())
```

### 3. Error Handling
Always handle API errors gracefully:

```python
try:
    response = await ai_service.generate_response(message)
except Exception as e:
    # Log error
    logger.error(f"AI generation error: {e}")
    # Return fallback response
    response = "I'm having trouble processing that right now. Please try again."
```

### 4. Monitor Usage
Track API usage and costs:

```python
import logging

logger = logging.getLogger(__name__)

async def generate_with_logging(message: str):
    """Generate response with usage logging."""
    start_time = time.time()
    
    response = await ai_service.generate_response(message)
    
    duration = time.time() - start_time
    logger.info(f"AI request: {len(message)} chars, {duration:.2f}s")
    
    return response
```

---

## 📊 Comparison of Free LLM Options

| Provider | Free Tier | Speed | Quality | Best For |
|----------|-----------|-------|---------|----------|
| **Gemini** | Generous | Fast | Excellent | General use, free forever |
| **Groq** | Good | **Fastest** | Very Good | Speed-critical apps |
| **OpenAI** | $5 credit | Fast | Excellent | Production apps |
| **Hugging Face** | Limited | Slow | Variable | Experimentation |
| **Anthropic** | Limited | Medium | Excellent | Complex reasoning |

**Recommendation**: Start with **Gemini** (free) or **Groq** (fast & free), then upgrade to **OpenAI** for production.

---

## 🚀 Quick Start Commands

```bash
# 1. Install dependencies
pip install google-generativeai groq openai

# 2. Get API key from https://makersuite.google.com/app/apikey

# 3. Add to .env
echo "AI_PROVIDER=gemini" >> backend/.env
echo "GEMINI_API_KEY=your_key_here" >> backend/.env

# 4. Test the AI
cd backend
python test_real_ai.py

# 5. Start the server
python -m uvicorn main:app --reload
```

---

## 📖 Additional Resources

- **Gemini API Docs**: https://ai.google.dev/docs
- **Groq Documentation**: https://console.groq.com/docs
- **OpenAI API Reference**: https://platform.openai.com/docs
- **Bookkeeping Basics**: https://www.sba.gov/business-guide/manage-your-business/bookkeeping-accounting
- **Small Business Tax Guide**: https://www.irs.gov/businesses/small-businesses-self-employed

---

## 🎓 Next Steps

1. **Get API Key**: Sign up for Gemini or Groq
2. **Implement AI Service**: Follow implementation guide above
3. **Test Responses**: Run test script with various queries
4. **Fine-tune Prompts**: Adjust system prompt based on responses
5. **Monitor Usage**: Track API calls and costs
6. **Optimize**: Cache common queries, implement rate limiting
7. **Deploy**: Move to production with proper error handling

---

**Need Help?** Check the provider documentation or test with the mock assistant first to understand expected behavior.
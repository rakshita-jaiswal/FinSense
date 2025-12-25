"""Mock AI Assistant service for generating intelligent financial responses."""
import random
from typing import List, Dict
from datetime import datetime


class MockAIAssistant:
    """Mock AI Assistant that generates contextual financial responses."""
    
    def __init__(self):
        self.greeting_responses = [
            "Hello! I'm FinAI, your financial assistant. How can I help you manage your business finances today?",
            "Hi there! I'm here to help you understand your financial data. What would you like to know?",
            "Welcome! I can help you analyze transactions, track expenses, and provide financial insights. What's on your mind?",
        ]
        
        self.transaction_keywords = ["transaction", "payment", "expense", "revenue", "income", "spent", "earned"]
        self.category_keywords = ["category", "categories", "categorize", "type", "kind"]
        self.summary_keywords = ["summary", "overview", "total", "how much", "profit", "loss"]
        self.trend_keywords = ["trend", "pattern", "growth", "increase", "decrease", "change"]
        self.help_keywords = ["help", "what can you do", "capabilities", "features"]
    
    async def generate_response(self, user_message: str, user_data: Dict = None) -> str:
        """
        Generate a contextual AI response based on user message and financial data.
        
        Args:
            user_message: The user's question or message
            user_data: Optional dictionary containing user's financial data
        
        Returns:
            AI-generated response string
        """
        message_lower = user_message.lower()
        
        # Greeting detection
        if any(word in message_lower for word in ["hello", "hi", "hey", "greetings"]):
            return random.choice(self.greeting_responses)
        
        # Help request
        if any(keyword in message_lower for keyword in self.help_keywords):
            return self._generate_help_response()
        
        # Transaction queries
        if any(keyword in message_lower for keyword in self.transaction_keywords):
            return self._generate_transaction_response(message_lower, user_data)
        
        # Category queries
        if any(keyword in message_lower for keyword in self.category_keywords):
            return self._generate_category_response(message_lower, user_data)
        
        # Summary/Overview queries
        if any(keyword in message_lower for keyword in self.summary_keywords):
            return self._generate_summary_response(message_lower, user_data)
        
        # Trend analysis queries
        if any(keyword in message_lower for keyword in self.trend_keywords):
            return self._generate_trend_response(message_lower, user_data)
        
        # Default response for unrecognized queries
        return self._generate_default_response(user_message)
    
    def _generate_help_response(self) -> str:
        """Generate help/capabilities response."""
        return """I can help you with various financial tasks:

**Financial Analysis**
- View transaction summaries and totals
- Analyze spending patterns by category
- Track revenue and expense trends

**Transaction Insights**
- Find specific transactions
- Categorize expenses
- Identify unusual spending

**Business Intelligence**
- Revenue vs expense comparisons
- Profit margin analysis
- Cash flow insights

**Quick Actions**
- "Show me my recent transactions"
- "What's my total revenue this month?"
- "Which category am I spending most on?"
- "How is my business performing?"

Just ask me anything about your finances, and I'll do my best to help!"""
    
    def _generate_transaction_response(self, message: str, user_data: Dict = None) -> str:
        """Generate response about transactions."""
        if "recent" in message or "latest" in message:
            return """Here are your most recent transactions:

1. **Daily Sales** - $450.75 (Revenue) - Today
2. **Sysco** - $325.50 (Inventory) - Yesterday
3. **Square Payroll** - $2,850.00 (Payroll) - 2 days ago
4. **Con Edison** - $285.40 (Utilities) - 3 days ago
5. **Online Orders** - $680.25 (Revenue) - 3 days ago

Would you like more details about any of these transactions?"""
        
        if "how many" in message:
            return """You currently have **75 transactions** in your system:
- **30 revenue transactions** totaling $15,234.56
- **45 expense transactions** totaling $11,789.23

Your transactions span the last 30 days. Would you like to see a breakdown by category?"""
        
        return """I can help you with transaction-related queries. Try asking:
- "Show me my recent transactions"
- "How many transactions do I have?"
- "What was my largest expense?"
- "Find transactions from last week"

What would you like to know about your transactions?"""
    
    def _generate_category_response(self, message: str, user_data: Dict = None) -> str:
        """Generate response about categories."""
        if "most" in message or "highest" in message or "top" in message:
            return """Your **top spending categories** are:

1. **Payroll** - $8,550.00 (38%)
2. **Inventory - Food & Supplies** - $6,234.80 (28%)
3. **Utilities** - $2,456.20 (11%)
4. **Marketing** - $1,890.45 (8%)
5. **Office Supplies** - $845.60 (4%)

Payroll is your largest expense category. This is typical for service-based businesses. Would you like suggestions on optimizing any category?"""
        
        if "list" in message or "all" in message or "what" in message:
            return """Your business uses these expense categories:

**Revenue:**
- Revenue (Sales & Income)

**Operating Expenses:**
- Inventory - Food & Supplies
- Payroll
- Utilities
- Marketing
- Office Supplies
- Professional Fees
- Repairs & Maintenance

All your transactions are automatically categorized with AI confidence scores. Would you like to review any specific category?"""
        
        return """I can help you understand your spending by category. Try asking:
- "What are my top spending categories?"
- "List all my expense categories"
- "How much did I spend on inventory?"
- "Show me my marketing expenses"

What category information would you like to see?"""
    
    def _generate_summary_response(self, message: str, user_data: Dict = None) -> str:
        """Generate financial summary response."""
        return """Here's your **financial summary** for the last 30 days:

**Revenue**
- Total: $15,234.56
- Transactions: 30
- Average: $507.82 per transaction

**Expenses**
- Total: $11,789.23
- Transactions: 45
- Average: $261.98 per transaction

**Net Profit**
- **$3,445.33** (22.6% profit margin)
- Up 8.5% compared to previous period

**Key Insights:**
- Your revenue is growing steadily
- Payroll is your largest expense (38%)
- Profit margin is healthy for your industry

Would you like a deeper analysis of any specific area?"""
    
    def _generate_trend_response(self, message: str, user_data: Dict = None) -> str:
        """Generate trend analysis response."""
        return """Here's your **financial trend analysis**:

**Revenue Trends**
- Last 7 days: $4,567.89
- Previous 7 days: $4,123.45
- Change: Up 10.8% (Growing!)

**Expense Trends**
- Last 7 days: $3,234.56
- Previous 7 days: $3,456.78
- Change: Down 6.4% (Decreasing)

**Profit Trends**
- Current week profit: $1,333.33
- Previous week profit: $666.67
- Change: Up 100% (Excellent!)

**Observations:**
- Your revenue is trending upward
- Expenses are under control
- Profit margin is improving

Keep up the good work! Would you like specific recommendations to maintain this trend?"""
    
    def _generate_default_response(self, message: str) -> str:
        """Generate default response for unrecognized queries."""
        responses = [
            f"I understand you're asking about '{message}'. Let me help you with that. Could you provide more details about what financial information you're looking for?",
            f"That's an interesting question about '{message}'. I can help you analyze your financial data. What specific aspect would you like to explore?",
            f"I'd be happy to help with '{message}'. To give you the most accurate information, could you clarify what financial metrics or transactions you're interested in?",
        ]
        
        return random.choice(responses) + "\n\nYou can ask me about:\n- Transaction summaries\n- Spending by category\n- Revenue and profit trends\n- Recent financial activity"


# Singleton instance
ai_assistant = MockAIAssistant()
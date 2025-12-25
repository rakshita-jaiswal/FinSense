"""Real AI service using Google Gemini API with rate limiting and caching."""
from typing import Dict, Optional, List
import re
import google.generativeai as genai

from ai_config import ai_config
from services.rate_limiter import ai_rate_limiter
from services.response_cache import response_cache
from services.sample_responses import initialize_cache_with_samples


class AIService:
    """AI service for generating intelligent responses using Google Gemini."""
    
    def __init__(self):
        """Initialize Gemini AI service."""
        # Configure Gemini with API key
        genai.configure(api_key=ai_config.GEMINI_API_KEY)
        
        # Initialize the model
        self.model = genai.GenerativeModel(
            model_name=ai_config.GEMINI_MODEL,
            generation_config={
                "temperature": ai_config.TEMPERATURE,
                "top_p": ai_config.TOP_P,
                "max_output_tokens": ai_config.MAX_TOKENS,
            }
        )
        
        print(f"[AI Service] Initialized with Gemini model: {ai_config.GEMINI_MODEL}")
        
        # Initialize cache with sample responses
        initialize_cache_with_samples()
    
    def _strip_markdown(self, text: str) -> str:
        """Remove markdown formatting from text."""
        # Remove bold (**text** or __text__)
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        text = re.sub(r'__(.+?)__', r'\1', text)
        
        # Remove italic (*text* or _text_)
        text = re.sub(r'\*(.+?)\*', r'\1', text)
        text = re.sub(r'_(.+?)_', r'\1', text)
        
        # Remove headers (## text)
        text = re.sub(r'^#{1,6}\s+(.+)$', r'\1', text, flags=re.MULTILINE)
        
        # Remove inline code (`text`)
        text = re.sub(r'`(.+?)`', r'\1', text)
        
        # Remove code blocks (```text```)
        text = re.sub(r'```[\s\S]*?```', '', text)
        
        return text
    
    async def generate_response(
        self,
        user_message: str,
        conversation_history: List[Dict] = None,
        user_data: Dict = None
    ) -> str:
        """
        Generate AI response using Google Gemini with caching and rate limiting.
        
        Args:
            user_message: User's question
            conversation_history: Previous messages for context
            user_data: User's financial data for personalized responses
        
        Returns:
            AI-generated response
        """
        try:
            # Check cache first (only for first message in conversation)
            if not conversation_history or len(conversation_history) == 0:
                cached_response = response_cache.get(user_message, user_data)
                if cached_response:
                    return cached_response
            
            # Acquire rate limit permission (will wait if necessary)
            await ai_rate_limiter.acquire()
            
            # Build context from user data
            context = self._build_context(user_data)
            
            # Build full prompt
            full_prompt = self._build_prompt(user_message, context, conversation_history)
            
            # Generate response
            response = self.model.generate_content(full_prompt)
            
            # Strip markdown formatting
            clean_response = self._strip_markdown(response.text)
            
            # Cache the response (only for first message in conversation)
            if not conversation_history or len(conversation_history) == 0:
                response_cache.set(user_message, clean_response, user_data)
            
            return clean_response
            
        except Exception as e:
            error_msg = str(e)
            print(f"[AI Service] Error generating response: {error_msg}")
            
            # Check if it's a rate limit error
            if "429" in error_msg or "quota" in error_msg.lower():
                return "I'm currently experiencing high demand. Please wait a moment and try again. Your question is important to me!"
            
            # Return fallback response for other errors
            return "I'm having trouble processing that right now. Please try asking your question in a different way, or try again in a moment."
    
    async def get_rate_limit_status(self) -> dict:
        """
        Get current rate limit status.
        
        Returns:
            Dictionary with rate limit statistics
        """
        return ai_rate_limiter.get_current_usage()
    
    def get_cache_stats(self) -> dict:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        return response_cache.get_stats()
    
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
            profit = user_data['profit']
            context_parts.append(f"Net Profit: ${profit:,.2f}")
            
            # Add profit margin if we have revenue
            if "revenue" in user_data and user_data['revenue'] > 0:
                margin = (profit / user_data['revenue']) * 100
                context_parts.append(f"Profit Margin: {margin:.1f}%")
        
        if "top_categories" in user_data and user_data['top_categories']:
            categories = ", ".join(user_data['top_categories'][:3])
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
        conversation_history: List[Dict] = None
    ) -> str:
        """Build complete prompt with system instructions and context."""
        prompt_parts = [ai_config.SYSTEM_PROMPT]
        
        # Add user's financial context if available
        if context:
            prompt_parts.append(context)
        
        # Add conversation history for context (last 5 messages)
        if conversation_history and len(conversation_history) > 0:
            prompt_parts.append("\n\nConversation History:")
            for msg in conversation_history[-5:]:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                prompt_parts.append(f"{role.capitalize()}: {content}")
        
        # Add current user question
        prompt_parts.append(f"\n\nUser Question: {user_message}")
        prompt_parts.append("\n\nAssistant Response:")
        
        return "\n".join(prompt_parts)


# Singleton instance
ai_service = AIService()
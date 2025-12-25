"""Response cache for AI queries to reduce API calls."""
import hashlib
import json
from typing import Optional, Dict
from datetime import datetime, timedelta


class ResponseCache:
    """
    Cache for AI responses to reduce API calls.
    Uses in-memory storage with TTL (time-to-live).
    """
    
    def __init__(self, ttl_hours: int = 24):
        """
        Initialize response cache.
        
        Args:
            ttl_hours: Time-to-live for cached responses in hours
        """
        self.cache: Dict[str, dict] = {}
        self.ttl_hours = ttl_hours
        self.hits = 0
        self.misses = 0
    
    def _generate_key(self, user_message: str, user_data: Dict = None) -> str:
        """
        Generate cache key from user message and data.
        
        Args:
            user_message: User's question
            user_data: User's financial context (optional)
        
        Returns:
            Cache key (hash)
        """
        # Normalize message (lowercase, strip whitespace)
        normalized_message = user_message.lower().strip()
        
        # For general questions, ignore user_data
        # For personalized questions, include key financial metrics
        cache_data = {"message": normalized_message}
        
        if user_data and self._is_personalized_query(normalized_message):
            # Include only key metrics that affect the response
            cache_data["has_data"] = True
            if "profit" in user_data:
                # Round to nearest 1000 for caching purposes
                cache_data["profit_range"] = round(user_data["profit"] / 1000) * 1000
        
        # Generate hash
        cache_str = json.dumps(cache_data, sort_keys=True)
        return hashlib.md5(cache_str.encode()).hexdigest()
    
    def _is_personalized_query(self, message: str) -> bool:
        """Check if query requires personalized data."""
        personalized_keywords = [
            "my", "i am", "i'm", "should i", "am i",
            "my business", "my expenses", "my revenue"
        ]
        return any(keyword in message for keyword in personalized_keywords)
    
    def get(self, user_message: str, user_data: Dict = None) -> Optional[str]:
        """
        Get cached response if available and not expired.
        
        Args:
            user_message: User's question
            user_data: User's financial context
        
        Returns:
            Cached response or None
        """
        key = self._generate_key(user_message, user_data)
        
        if key in self.cache:
            entry = self.cache[key]
            
            # Check if expired
            if datetime.now() < entry["expires_at"]:
                self.hits += 1
                print(f"[Cache] HIT for: {user_message[:50]}...")
                return entry["response"]
            else:
                # Remove expired entry
                del self.cache[key]
        
        self.misses += 1
        print(f"[Cache] MISS for: {user_message[:50]}...")
        return None
    
    def set(self, user_message: str, response: str, user_data: Dict = None):
        """
        Cache a response.
        
        Args:
            user_message: User's question
            response: AI's response
            user_data: User's financial context
        """
        key = self._generate_key(user_message, user_data)
        
        self.cache[key] = {
            "response": response,
            "cached_at": datetime.now(),
            "expires_at": datetime.now() + timedelta(hours=self.ttl_hours),
            "message": user_message[:100]  # Store for debugging
        }
        
        print(f"[Cache] STORED: {user_message[:50]}...")
    
    def clear_expired(self):
        """Remove all expired entries from cache."""
        now = datetime.now()
        expired_keys = [
            key for key, entry in self.cache.items()
            if now >= entry["expires_at"]
        ]
        
        for key in expired_keys:
            del self.cache[key]
        
        if expired_keys:
            print(f"[Cache] Cleared {len(expired_keys)} expired entries")
    
    def get_stats(self) -> dict:
        """Get cache statistics."""
        total_requests = self.hits + self.misses
        hit_rate = (self.hits / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "total_entries": len(self.cache),
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": f"{hit_rate:.1f}%",
            "ttl_hours": self.ttl_hours
        }
    
    def clear(self):
        """Clear all cache entries."""
        self.cache.clear()
        self.hits = 0
        self.misses = 0
        print("[Cache] Cleared all entries")


# Global cache instance
response_cache = ResponseCache(ttl_hours=24)
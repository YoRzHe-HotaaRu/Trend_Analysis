import redis
import json
import logging
from datetime import datetime, timedelta
import os

logger = logging.getLogger(__name__)

class CacheManager:
    def __init__(self):
        self.redis_client = None
        self.memory_cache = {}  # Fallback to memory cache
        self.default_timeout = 300  # 5 minutes default
        
        # Try to initialize Redis connection
        try:
            redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379')
            self.redis_client = redis.from_url(redis_url, decode_responses=True)
            # Test connection
            self.redis_client.ping()
            logger.info("Redis cache initialized successfully")
        except Exception as e:
            logger.warning(f"Redis cache not available, using memory cache: {e}")
            self.redis_client = None

    def get(self, key):
        """Get data from cache"""
        try:
            if self.redis_client:
                # Try Redis first
                value = self.redis_client.get(key)
                if value:
                    return json.loads(value)
            else:
                # Fallback to memory cache
                if key in self.memory_cache:
                    cache_item = self.memory_cache[key]
                    # Check if expired
                    if cache_item['expires_at'] > datetime.now():
                        return cache_item['data']
                    else:
                        # Remove expired item
                        del self.memory_cache[key]
            
            return None
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None

    def set(self, key, value, timeout=None):
        """Set data in cache"""
        try:
            if timeout is None:
                timeout = self.default_timeout
            
            if self.redis_client:
                # Use Redis
                self.redis_client.setex(key, timeout, json.dumps(value, default=str))
            else:
                # Use memory cache
                expires_at = datetime.now() + timedelta(seconds=timeout)
                self.memory_cache[key] = {
                    'data': value,
                    'expires_at': expires_at
                }
                # Clean up old entries occasionally
                if len(self.memory_cache) > 1000:
                    self._cleanup_memory_cache()
                    
            logger.debug(f"Cache set: {key}")
        except Exception as e:
            logger.error(f"Cache set error: {e}")

    def delete(self, key):
        """Delete data from cache"""
        try:
            if self.redis_client:
                self.redis_client.delete(key)
            else:
                if key in self.memory_cache:
                    del self.memory_cache[key]
                    
            logger.debug(f"Cache deleted: {key}")
        except Exception as e:
            logger.error(f"Cache delete error: {e}")

    def flush(self):
        """Clear all cache"""
        try:
            if self.redis_client:
                self.redis_client.flushdb()
            else:
                self.memory_cache.clear()
                
            logger.info("Cache flushed")
        except Exception as e:
            logger.error(f"Cache flush error: {e}")

    def _cleanup_memory_cache(self):
        """Clean up expired items from memory cache"""
        now = datetime.now()
        expired_keys = [
            key for key, item in self.memory_cache.items()
            if item['expires_at'] <= now
        ]
        for key in expired_keys:
            del self.memory_cache[key]
        
        if expired_keys:
            logger.debug(f"Cleaned up {len(expired_keys)} expired cache items")

# Global cache manager instance
cache_manager = CacheManager()
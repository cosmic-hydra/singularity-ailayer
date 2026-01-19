"""Performance optimization and caching module.

This module provides caching and optimization features to enable
faster navigation and task execution.
"""
import functools
import hashlib
import json
import time
from pathlib import Path
from typing import Any, Callable, Dict, Optional

from .config import get_settings
from .logging_config import get_logger

logger = get_logger(__name__)
settings = get_settings()


class PerformanceCache:
    """In-memory and disk cache for faster task execution."""

    def __init__(self, cache_dir: Optional[Path] = None):
        """Initialize the performance cache.

        Args:
            cache_dir: Optional directory for persistent cache storage
        """
        self.memory_cache: Dict[str, tuple[Any, float]] = {}
        self.cache_dir = cache_dir or Path.home() / ".singularity_cache"
        self.cache_ttl = 3600  # 1 hour default TTL
        self.max_memory_items = 100

        # Create cache directory if it doesn't exist
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        logger.info("Performance cache initialized", cache_dir=str(self.cache_dir))

    def get(self, key: str) -> Optional[Any]:
        """Get item from cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found or expired
        """
        # Check memory cache first
        if key in self.memory_cache:
            value, timestamp = self.memory_cache[key]
            if time.time() - timestamp < self.cache_ttl:
                logger.debug("Cache hit (memory)", key=key)
                return value
            else:
                # Remove expired item
                del self.memory_cache[key]

        # Check disk cache
        cache_file = self.cache_dir / f"{self._hash_key(key)}.json"
        if cache_file.exists():
            try:
                with open(cache_file, "r") as f:
                    data = json.load(f)
                    timestamp = data.get("timestamp", 0)
                    if time.time() - timestamp < self.cache_ttl:
                        value = data.get("value")
                        # Promote to memory cache
                        self._add_to_memory(key, value, timestamp)
                        logger.debug("Cache hit (disk)", key=key)
                        return value
            except Exception as e:
                logger.error("Error reading from disk cache", key=key, error=str(e))

        logger.debug("Cache miss", key=key)
        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set item in cache.

        Args:
            key: Cache key
            value: Value to cache
            ttl: Optional time-to-live in seconds (overrides default)
        """
        timestamp = time.time()
        cache_ttl = ttl if ttl is not None else self.cache_ttl

        # Add to memory cache
        self._add_to_memory(key, value, timestamp)

        # Write to disk cache for persistence
        cache_file = self.cache_dir / f"{self._hash_key(key)}.json"
        try:
            with open(cache_file, "w") as f:
                json.dump({"value": value, "timestamp": timestamp, "ttl": cache_ttl}, f)
            logger.debug("Item cached", key=key)
        except Exception as e:
            logger.error("Error writing to disk cache", key=key, error=str(e))

    def invalidate(self, key: str):
        """Invalidate a cache entry.

        Args:
            key: Cache key to invalidate
        """
        # Remove from memory
        if key in self.memory_cache:
            del self.memory_cache[key]

        # Remove from disk
        cache_file = self.cache_dir / f"{self._hash_key(key)}.json"
        if cache_file.exists():
            cache_file.unlink()

        logger.debug("Cache invalidated", key=key)

    def clear(self):
        """Clear all cache entries."""
        self.memory_cache.clear()

        # Clear disk cache
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()

        logger.info("Cache cleared")

    def _add_to_memory(self, key: str, value: Any, timestamp: float):
        """Add item to memory cache with size limit."""
        # Evict oldest items if cache is full
        if len(self.memory_cache) >= self.max_memory_items:
            oldest_key = min(self.memory_cache.keys(), key=lambda k: self.memory_cache[k][1])
            del self.memory_cache[oldest_key]

        self.memory_cache[key] = (value, timestamp)

    def _hash_key(self, key: str) -> str:
        """Generate a hash for the cache key."""
        return hashlib.md5(key.encode()).hexdigest()


# Global cache instance
_cache: Optional[PerformanceCache] = None


def get_cache() -> PerformanceCache:
    """Get or create the global performance cache instance."""
    global _cache
    if _cache is None:
        _cache = PerformanceCache()
    return _cache


def cached(ttl: Optional[int] = None):
    """Decorator to cache function results.

    Args:
        ttl: Optional time-to-live in seconds

    Example:
        @cached(ttl=300)
        def expensive_function(arg1, arg2):
            # ... expensive computation
            return result
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key from function name and arguments
            key_parts = [func.__name__, str(args), str(sorted(kwargs.items()))]
            cache_key = "|".join(key_parts)

            # Try to get from cache
            cache = get_cache()
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result

            # Execute function and cache result
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl=ttl)
            return result

        return wrapper

    return decorator

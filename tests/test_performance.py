"""Tests for performance optimization module."""
import time

import pytest


class TestPerformanceCache:
    """Tests for PerformanceCache class."""

    def test_cache_initialization(self, tmp_path):
        """Test cache initializes correctly."""
        from core.performance import PerformanceCache

        cache = PerformanceCache(cache_dir=tmp_path)
        assert cache.cache_dir == tmp_path
        assert len(cache.memory_cache) == 0

    def test_cache_set_and_get(self, tmp_path):
        """Test setting and getting cache values."""
        from core.performance import PerformanceCache

        cache = PerformanceCache(cache_dir=tmp_path)

        # Set a value
        cache.set("test_key", {"data": "test_value"})

        # Get the value
        result = cache.get("test_key")
        assert result == {"data": "test_value"}

    def test_cache_expiration(self, tmp_path):
        """Test cache expiration."""
        from core.performance import PerformanceCache

        cache = PerformanceCache(cache_dir=tmp_path)
        cache.cache_ttl = 1  # 1 second TTL

        # Set a value
        cache.set("test_key", "test_value")

        # Should exist immediately
        assert cache.get("test_key") == "test_value"

        # Wait for expiration
        time.sleep(1.5)

        # Should be expired
        assert cache.get("test_key") is None

    def test_cache_invalidation(self, tmp_path):
        """Test cache invalidation."""
        from core.performance import PerformanceCache

        cache = PerformanceCache(cache_dir=tmp_path)

        cache.set("test_key", "test_value")
        assert cache.get("test_key") == "test_value"

        cache.invalidate("test_key")
        assert cache.get("test_key") is None

    def test_cache_clear(self, tmp_path):
        """Test clearing all cache."""
        from core.performance import PerformanceCache

        cache = PerformanceCache(cache_dir=tmp_path)

        cache.set("key1", "value1")
        cache.set("key2", "value2")

        cache.clear()

        assert cache.get("key1") is None
        assert cache.get("key2") is None

    def test_cached_decorator(self, tmp_path):
        """Test cached decorator."""
        from core.performance import cached, PerformanceCache, get_cache

        # Reset cache
        cache = PerformanceCache(cache_dir=tmp_path)

        call_count = {"value": 0}

        @cached(ttl=60)
        def expensive_function(x):
            call_count["value"] += 1
            return x * 2

        # First call
        result1 = expensive_function(5)
        assert result1 == 10
        assert call_count["value"] == 1

        # Second call should use cache
        result2 = expensive_function(5)
        assert result2 == 10
        assert call_count["value"] == 1  # Not incremented

    def test_memory_cache_size_limit(self, tmp_path):
        """Test memory cache size limit."""
        from core.performance import PerformanceCache

        cache = PerformanceCache(cache_dir=tmp_path)
        cache.max_memory_items = 5

        # Add more items than limit
        for i in range(10):
            cache.set(f"key{i}", f"value{i}")

        # Memory cache should not exceed limit
        assert len(cache.memory_cache) <= 5

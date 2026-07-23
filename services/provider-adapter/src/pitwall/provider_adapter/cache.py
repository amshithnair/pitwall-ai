import json
from typing import Any

import redis


class ProviderCache:
    """Redis-backed cache for provider data."""

    def __init__(self):
        self.redis = redis.Redis(host="redis", port=6379, decode_responses=True)
        self.ttl = 86400 * 7  # 7 days

    def get(self, key: str) -> Any | None:
        val = self.redis.get(key)
        if val:
            return json.loads(val)
        return None

    def set(self, key: str, value: Any):
        self.redis.setex(key, self.ttl, json.dumps(value))

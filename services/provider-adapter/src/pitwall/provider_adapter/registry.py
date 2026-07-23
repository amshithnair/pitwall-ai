from pitwall.provider_adapter.base import BaseProvider
from pitwall.provider_adapter.providers.fastf1_provider import FastF1Provider


class ProviderRegistry:
    """Registry describing capabilities of all providers."""

    def __init__(self):
        self._providers = {
            "fastf1": {
                "instance": FastF1Provider(),
                "capabilities": {
                    "historical": True,
                    "live": False,
                    "telemetry": True,
                    "weather": True,
                    "limitations": "Live timing is not officially supported.",
                },
            }
        }

    def get_provider(self, name: str) -> BaseProvider:
        provider_info = self._providers.get(name.lower())
        if provider_info:
            return provider_info["instance"]
        return None

    def list_providers(self) -> dict:
        return {k: v["capabilities"] for k, v in self._providers.items()}

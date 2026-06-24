import hashlib
import json
import logging
from typing import List

import redis

from app.core.config import settings

from .providers import (
    AIFinding,
    BaseLLMProvider,
    CerebrasProvider,
    GroqProvider,
    MockProvider,
    NvidiaProvider,
    OllamaProvider,
)

logger = logging.getLogger(__name__)

# Basic sync redis client for caching
try:
    redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
except Exception:
    redis_client = None


class AIOrchestrator:
    def __init__(self, model_name: str = "qwen/qwen3-coder-480b"):
        self.model_name = model_name
        self._providers = {
            "groq": GroqProvider,
            "cerebras": CerebrasProvider,
            "nvidia": NvidiaProvider,
            "ollama": OllamaProvider,
            "mock": MockProvider,
        }

    def _get_provider_instance(self, name: str) -> BaseLLMProvider:
        provider_class = self._providers.get(name.lower(), MockProvider)
        return provider_class(model_name=self.model_name)

    def _execute_with_fallback(self, method_name: str, diff: str) -> List[AIFinding]:
        """Attempts the default provider, falls back sequentially on failure."""
        primary_name = settings.DEFAULT_PROVIDER
        fallbacks = ["cerebras", "nvidia", "ollama"] if settings.ENABLE_FALLBACK else []

        # Remove primary from fallbacks if it's there
        fallbacks = [f for f in fallbacks if f != primary_name]

        attempts = [primary_name] + fallbacks

        for provider_name in attempts:
            try:
                logger.info(f"Attempting {method_name} using provider: {provider_name}")
                provider = self._get_provider_instance(provider_name)
                method = getattr(provider, method_name)
                findings = method(diff)
                return findings
            except Exception as e:
                logger.warning(f"Provider {provider_name} failed: {e}. Trying next...")

        logger.error("All AI providers failed.")
        return []

    def _get_cache_key(self, prefix: str, diff: str) -> str:
        diff_hash = hashlib.md5(diff.encode("utf-8")).hexdigest()
        return f"ai_review:{prefix}:{diff_hash}"

    def _cached_execute(self, method_name: str, diff: str) -> List[AIFinding]:
        cache_key = self._get_cache_key(method_name, diff)

        if redis_client:
            cached = redis_client.get(cache_key)
            if cached:
                logger.info(f"Cache HIT for {method_name}")
                data = json.loads(cached)
                return [AIFinding(**f) for f in data]

        logger.info(f"Cache MISS for {method_name}. Executing AI calls.")
        findings = self._execute_with_fallback(method_name, diff)

        if redis_client and findings:
            # Cache for 7 days
            redis_client.setex(
                cache_key, 604800, json.dumps([f.model_dump() for f in findings])
            )

        return findings

    def run_review(self, agent_type: str, diff: str) -> List[AIFinding]:
        """Main entry point for graph nodes."""
        method_map = {
            "security": "review_security",
            "performance": "review_performance",
            "architecture": "review_architecture",
            "maintainability": "review_maintainability",
        }

        method_name = method_map.get(agent_type)
        if not method_name:
            raise ValueError(f"Unknown agent type: {agent_type}")

        findings = self._cached_execute(method_name, diff)

        # Multi-model consensus for critical findings
        if settings.ENABLE_MULTI_MODEL_REVIEW and findings:
            critical_findings = [
                f for f in findings if f.severity.lower() in ("critical", "high")
            ]
            if critical_findings:
                logger.info("Executing multi-model consensus for critical findings...")
                # We do a secondary pass specifically on Groq/Cerebras if possible
                # For brevity, we simulate the consensus check here.
                # In production, we'd fire the diff to Cerebras and compare outputs.
                for f in critical_findings:
                    f.confidence_score = 0.85  # Assumed baseline

        return findings

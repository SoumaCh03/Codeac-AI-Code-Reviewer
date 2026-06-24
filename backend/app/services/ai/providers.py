import logging
from abc import ABC, abstractmethod
from typing import List

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from app.core.config import settings

logger = logging.getLogger(__name__)


class AIFinding(BaseModel):
    severity: str = Field(description="One of: critical, high, medium, low, info")
    category: str = Field(
        description="The category: security, performance, architecture, maintainability"
    )
    title: str = Field(description="A short, descriptive title of the finding")
    explanation: str = Field(description="Detailed explanation of why this is an issue")
    code_reference: str = Field(
        description="The specific file path and/or snippet where the issue is located"
    )
    suggested_fix: str = Field(
        description="Actionable suggested fix with code snippets if relevant"
    )
    confidence_score: float = Field(description="Confidence from 0.0 to 1.0")


class AIFindingList(BaseModel):
    findings: List[AIFinding]


class BaseLLMProvider(ABC):
    def __init__(self, model_name: str, temperature: float = 0.0):
        self.model_name = model_name
        self.temperature = temperature
        self.llm = self._initialize_llm().with_structured_output(AIFindingList)

    @abstractmethod
    def _initialize_llm(self) -> ChatOpenAI:
        """Initialize the specific LangChain ChatModel with appropriate base_url and api_key."""

    def _execute_review(
        self, prompt_messages: List[tuple], diff: str
    ) -> List[AIFinding]:
        prompt = ChatPromptTemplate.from_messages(prompt_messages)
        chain = prompt | self.llm
        try:
            result = chain.invoke({"diff": diff})
            return result.findings if result and hasattr(result, "findings") else []
        except Exception as e:
            logger.error(f"{self.__class__.__name__} failed: {str(e)}")
            raise e

    def review_security(self, diff: str) -> List[AIFinding]:
        messages = [
            (
                "system",
                "You are an expert Security Engineer. Review the following Git Diff and find ONLY security vulnerabilities (OWASP Top 10, SQLi, XSS, CSRF, SSRF, RCE, Secrets). If no critical security issues are found, return an empty list.",
            ),
            ("user", "Diff to review:\n{diff}"),
        ]
        return self._execute_review(messages, diff)

    def review_performance(self, diff: str) -> List[AIFinding]:
        messages = [
            (
                "system",
                "You are a Staff Backend Engineer. Review the following Git Diff and find ONLY severe performance bottlenecks (N+1 queries, memory leaks, blocking I/O, O(N^2) loops). Provide optimized alternatives. If none are found, return an empty list.",
            ),
            ("user", "Diff to review:\n{diff}"),
        ]
        return self._execute_review(messages, diff)

    def review_architecture(self, diff: str) -> List[AIFinding]:
        messages = [
            (
                "system",
                "You are a Principal Architect. Review the Git Diff and point out ONLY major architectural smells (tight coupling, breaking SOLID, god objects). Provide clear refactoring suggestions. Ignore minor style issues.",
            ),
            ("user", "Diff to review:\n{diff}"),
        ]
        return self._execute_review(messages, diff)

    def review_maintainability(self, diff: str) -> List[AIFinding]:
        messages = [
            (
                "system",
                "You are a Senior Developer. Review the Git Diff for maintainability issues (long functions, poor naming, missing tests, high cyclomatic complexity). If code is clean, return an empty list.",
            ),
            ("user", "Diff to review:\n{diff}"),
        ]
        return self._execute_review(messages, diff)


class GroqProvider(BaseLLMProvider):
    def _initialize_llm(self) -> ChatOpenAI:
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY missing")
        return ChatOpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=settings.GROQ_API_KEY,
            model=self.model_name,
            temperature=self.temperature,
        )


class CerebrasProvider(BaseLLMProvider):
    def _initialize_llm(self) -> ChatOpenAI:
        if not settings.CEREBRAS_API_KEY:
            raise ValueError("CEREBRAS_API_KEY missing")
        return ChatOpenAI(
            base_url="https://api.cerebras.ai/v1",
            api_key=settings.CEREBRAS_API_KEY,
            model=self.model_name,
            temperature=self.temperature,
        )


class NvidiaProvider(BaseLLMProvider):
    def _initialize_llm(self) -> ChatOpenAI:
        if not settings.NVIDIA_API_KEY:
            raise ValueError("NVIDIA_API_KEY missing")
        return ChatOpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=settings.NVIDIA_API_KEY,
            model="nvidia/nemotron-3-ultra-550b-a55b",  # Use specific model for NVIDIA
            temperature=self.temperature,
        )


class OllamaProvider(BaseLLMProvider):
    def _initialize_llm(self) -> ChatOpenAI:
        return ChatOpenAI(
            base_url=f"{settings.OLLAMA_BASE_URL}/v1",
            api_key="ollama",  # required but ignored by ollama
            model=self.model_name,
            temperature=self.temperature,
        )


class MockProvider(BaseLLMProvider):
    def _initialize_llm(self) -> ChatOpenAI:
        return ChatOpenAI(api_key="mock", model="mock")

    def _execute_review(
        self, prompt_messages: List[tuple], diff: str
    ) -> List[AIFinding]:
        return [
            AIFinding(
                severity="low",
                category="maintainability",
                title="Mock finding",
                explanation="This is a mocked finding from the fallback testing provider.",
                code_reference="N/A",
                suggested_fix="N/A",
                confidence_score=0.9,
            )
        ]

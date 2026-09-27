import os
import logging
from pathlib import Path
from typing import Optional
from fastapi import HTTPException
from groq import AsyncGroq
from dotenv import load_dotenv
from backend.config import settings

logger = logging.getLogger("deal_intelligence.llm")

class LLMService:
    def _get_client(self) -> AsyncGroq:
        root_dir = Path(__file__).resolve().parent.parent.parent
        env_path = root_dir / ".env"
        if env_path.exists():
            load_dotenv(dotenv_path=env_path, override=True)

        key = os.getenv("GROQ_API_KEY", settings.GROQ_API_KEY or "").strip()
        if not key:
            raise HTTPException(
                status_code=503,
                detail="LLM provider API key not configured. Unable to generate grounded AI reasoning."
            )
        return AsyncGroq(api_key=key)

    async def check_health(self) -> str:
        """
        Check real connectivity to Groq LLM API.
        Returns 'healthy' or 'unhealthy'.
        """
        try:
            client = self._get_client()
            models = await client.models.list()
            if models:
                return "healthy"
            return "unhealthy"
        except Exception as e:
            logger.warning(f"LLM Health Check Failed: {str(e)}")
            return "unhealthy"

    async def generate_completion(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
        model: str = "openai/gpt-oss-120b"
    ) -> str:
        client = self._get_client()
        candidate_models = [model, "openai/gpt-oss-120b", "qwen/qwen3.8-27b", "openai/gpt-oss-20b"]

        last_error = None
        for m in candidate_models:
            try:
                response = await client.chat.completions.create(
                    model=m,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=temperature,
                    max_tokens=2048
                )
                content = response.choices[0].message.content
                if content:
                    return content
            except Exception as e:
                logger.warning(f"Groq LLM model '{m}' failed: {e}")
                last_error = e
                continue

        logger.error(f"All LLM candidate models failed. Last error: {last_error}")
        raise HTTPException(
            status_code=503,
            detail=f"LLM provider unavailable. Unable to generate a grounded response. ({str(last_error)})"
        )

llm_service = LLMService()

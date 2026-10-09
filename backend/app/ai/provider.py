"""AI extraction providers. Live Gemma inference is explicitly opt-in."""
import base64
import json
import os
import re
from pathlib import Path

import httpx
from dotenv import load_dotenv

from .base import ExtractionProvider, PageMetadata
from .prompts import EXTRACTION_SYSTEM_PROMPT
from .validation import validate_records

# Load the project-root .env for local development. Deployment environment variables
# take precedence and secrets must never be committed.
load_dotenv(Path(__file__).resolve().parents[3] / ".env", override=False)


class MockProvider(ExtractionProvider):
    async def extract(self, page_image: bytes, metadata: PageMetadata):
        # Stable demo fixture; this is NOT OCR of the supplied image.
        payload = [{
            "serial_number": {"value": 1, "source_text": "1", "confidence": 0.99,
                              "bbox": {"x": 0.05, "y": 0.1, "width": 0.05, "height": 0.03}, "status": "observed"},
            "voter_id": {"value": None, "status": "missing"},
            "name": {"value": "DEMO RECORD", "source_text": "DEMO RECORD", "confidence": 0.95,
                     "bbox": {"x": 0.12, "y": 0.1, "width": 0.25, "height": 0.04}, "status": "observed"},
            "relative_name": {"value": None, "status": "missing"},
            "house_number": {"value": None, "status": "missing"},
            "age": {"value": None, "status": "missing"},
            "gender": {"value": None, "status": "missing"},
            "page_number": metadata.page_number, "provenance": "mock", "review_status": "unreviewed"
        }]
        return validate_records(payload, metadata.page_number, "mock")


class GemmaProvider(ExtractionProvider):
    """Calls Google's hosted Gemma model through the Gemini API REST endpoint."""

    def __init__(self):
        self.base_url = os.getenv(
            "ROLLLENS_AI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta"
        ).rstrip("/")
        self.model = os.getenv("ROLLLENS_AI_MODEL", "gemma-4-26b-a4b-it")
        self.api_key = os.getenv("ROLLLENS_AI_API_KEY", "")
        if not self.api_key:
            raise RuntimeError("Live AI requires ROLLLENS_AI_API_KEY")
        if not self.model or "/" in self.model:
            raise RuntimeError("ROLLLENS_AI_MODEL must be a model ID such as gemma-4-26b-a4b-it")

    async def extract(self, page_image: bytes, metadata: PageMetadata):
        schema_instructions = f"""
{EXTRACTION_SYSTEM_PROMPT}
Return ONLY a valid JSON array. Each array item must have these top-level keys:
serial_number, voter_id, name, relative_name, house_number, age, gender,
page_number, provenance, review_status.
Each field except page_number/provenance/review_status must be an object with
value (string, integer, or null), source_text (string or null), confidence (0..1 or null),
bbox (object with normalized x,y,width,height or null), and status (observed, missing,
illegible, or needs_review). Use null bbox/confidence if uncertain. Never invent values.
Set page_number to {metadata.page_number}, provenance to "model", and review_status to "unreviewed".
If no records are visible, return []. Do not include markdown fences or commentary.
""".strip()
        body = {
            "systemInstruction": {"parts": [{"text": schema_instructions}]},
            "contents": [{"role": "user", "parts": [
                {"text": f"Extract the visible records from this page image. Language hint: {metadata.language_hint or 'unspecified'}."},
                {"inlineData": {"mimeType": "image/png", "data": base64.b64encode(page_image).decode("ascii")}}
            ]}],
            "generationConfig": {"temperature": 0.0, "maxOutputTokens": 8192}
        }
        url = f"{self.base_url}/models/{self.model}:generateContent"
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(90.0, connect=15.0)) as client:
                response = await client.post(
                    url,
                    headers={"x-goog-api-key": self.api_key, "Content-Type": "application/json"},
                    json=body,
                )
                response.raise_for_status()
                result = response.json()
        except httpx.HTTPStatusError as exc:
            # Avoid returning provider response bodies that could contain sensitive details.
            raise RuntimeError(f"Gemma API returned HTTP {exc.response.status_code}") from exc
        except httpx.RequestError as exc:
            raise RuntimeError("Could not reach the Gemma API; check network and API configuration") from exc

        try:
            text = result["candidates"][0]["content"]["parts"]
            output = "\n".join(part.get("text", "") for part in text).strip()
            output = re.sub(r"^```(?:json)?\s*|\s*```$", "", output, flags=re.IGNORECASE)
            payload = json.loads(output)
            if isinstance(payload, dict) and isinstance(payload.get("records"), list):
                payload = payload["records"]
            return validate_records(payload, metadata.page_number, "model")
        except (KeyError, IndexError, TypeError, json.JSONDecodeError, ValueError) as exc:
            raise RuntimeError("Gemma returned an invalid extraction response; no records were accepted") from exc


# Keep the old class name available for existing imports, but route it to Gemma's
# native REST contract rather than incorrectly assuming OpenAI compatibility.
OpenAICompatibleProvider = GemmaProvider


def get_provider() -> ExtractionProvider:
    mode = os.getenv("ROLLLENS_AI_PROVIDER", "mock").strip().lower()
    if mode == "mock":
        return MockProvider()
    if mode in {"gemma", "google", "google-gemma", "openai-compatible"}:
        return GemmaProvider()
    if mode in {"vllm", "ollama"}:
        raise RuntimeError(f"Provider '{mode}' is not implemented in this build; use 'gemma' or 'mock'")
    raise ValueError(f"unsupported ROLLLENS_AI_PROVIDER: {mode}")

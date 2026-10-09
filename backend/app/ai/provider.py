"""Replaceable provider factory. Live inference is deliberately opt-in."""
import asyncio, json, os
from .base import ExtractionProvider, PageMetadata
from .validation import validate_records

class MockProvider(ExtractionProvider):
    async def extract(self, page_image: bytes, metadata: PageMetadata):
        # Stable demo fixture; no claim that this is OCR of the supplied image.
        payload = [{"serial_number":{"value":1,"source_text":"1","confidence":0.99,"bbox":{"x":0.05,"y":0.1,"width":0.05,"height":0.03},"status":"observed"},
          "voter_id":{"value":None,"status":"missing"}, "name":{"value":"DEMO RECORD","source_text":"DEMO RECORD","confidence":0.95,"bbox":{"x":0.12,"y":0.1,"width":0.25,"height":0.04},"status":"observed"},
          "relative_name":{"value":None,"status":"missing"},"house_number":{"value":None,"status":"missing"},"age":{"value":None,"status":"missing"},"gender":{"value":None,"status":"missing"},
          "page_number":metadata.page_number,"provenance":"mock","review_status":"unreviewed"}]
        return validate_records(payload, metadata.page_number, "mock")

class OpenAICompatibleProvider(ExtractionProvider):
    """Minimal adapter for a configured OpenAI-compatible endpoint; optional dependency httpx."""
    def __init__(self):
        self.base_url = os.getenv("ROLLLENS_AI_BASE_URL", "").rstrip("/")
        self.model = os.getenv("ROLLLENS_AI_MODEL", "")
        self.api_key = os.getenv("ROLLLENS_AI_API_KEY", "")
        if not (self.base_url and self.model and self.api_key):
            raise RuntimeError("Live AI requires ROLLLENS_AI_BASE_URL, ROLLLENS_AI_MODEL and ROLLLENS_AI_API_KEY")

    async def extract(self, page_image: bytes, metadata: PageMetadata):
        # Endpoint-specific image payloads vary. Refuse to guess API compatibility.
        raise NotImplementedError("Configure and implement the selected runtime's image payload contract before enabling live inference")

def get_provider() -> ExtractionProvider:
    mode = os.getenv("ROLLLENS_AI_PROVIDER", "mock").lower()
    if mode == "mock": return MockProvider()
    if mode in {"openai-compatible", "vllm", "ollama"}: return OpenAICompatibleProvider()
    raise ValueError(f"unsupported ROLLLENS_AI_PROVIDER: {mode}")

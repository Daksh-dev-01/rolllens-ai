"""Provider-neutral multimodal extraction contracts."""
from abc import ABC, abstractmethod
from typing import Any, Literal
from pydantic import BaseModel, ConfigDict, Field

class BoundingBox(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    x: float = Field(ge=0, le=1)
    y: float = Field(ge=0, le=1)
    width: float = Field(gt=0, le=1)
    height: float = Field(gt=0, le=1)

    @classmethod
    def validate_box(cls, value: Any):
        box = cls.model_validate(value)
        if box.x + box.width > 1 or box.y + box.height > 1:
            raise ValueError("bounding box extends outside normalized page")
        return box

class ExtractedField(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    value: str | int | None = None
    source_text: str | None = None
    confidence: float | None = Field(default=None, ge=0, le=1)
    bbox: BoundingBox | None = None
    status: Literal["observed", "illegible", "missing", "needs_review"] = "observed"

class VoterRecord(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    serial_number: ExtractedField = Field(default_factory=lambda: ExtractedField(status="missing"))
    voter_id: ExtractedField = Field(default_factory=lambda: ExtractedField(status="missing"))
    name: ExtractedField = Field(default_factory=lambda: ExtractedField(status="missing"))
    relative_name: ExtractedField = Field(default_factory=lambda: ExtractedField(status="missing"))
    house_number: ExtractedField = Field(default_factory=lambda: ExtractedField(status="missing"))
    age: ExtractedField = Field(default_factory=lambda: ExtractedField(status="missing"))
    gender: ExtractedField = Field(default_factory=lambda: ExtractedField(status="missing"))
    page_number: int = Field(ge=1)
    provenance: Literal["model", "mock"]
    review_status: Literal["unreviewed", "human_verified", "needs_review"] = "unreviewed"

class PageMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")
    document_id: str
    version_id: str
    page_number: int = Field(ge=1)
    language_hint: str | None = None

class ExtractionProvider(ABC):
    @abstractmethod
    async def extract(self, page_image: bytes, metadata: PageMetadata) -> list[VoterRecord]:
        """Extract records from a rendered page. Never treat output as human-verified."""
        raise NotImplementedError

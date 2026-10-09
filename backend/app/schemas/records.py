from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Literal
class RecordInput(BaseModel):
    page_id: str
    external_id: str | None = None
    name: str | None = None
    age: int | None = Field(default=None, ge=0, le=120)
    gender: str | None = None
    house_number: str | None = None
    address: str | None = None
    extraction_confidence: float | None = Field(default=None, ge=0, le=1)
    verification_status: Literal["unverified", "verified", "needs_review"] = "unverified"
    bbox: list[float] | None = None
    source: Literal["extracted", "synthetic_demo", "manual"] = "extracted"
    @field_validator("bbox")
    @classmethod
    def valid_bbox(cls, v):
        if v is not None and (len(v) != 4 or any(x < 0 or x > 1 for x in v) or v[2] <= 0 or v[3] <= 0 or v[0] + v[2] > 1 or v[1] + v[3] > 1):
            raise ValueError("bbox must be normalized [x, y, width, height] within [0,1]")
        return v
class RecordOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str; page_id: str; external_id: str | None; name: str | None; age: int | None
    gender: str | None; house_number: str | None; address: str | None
    extraction_confidence: float | None; verification_status: str; bbox: list[float] | None; source: str

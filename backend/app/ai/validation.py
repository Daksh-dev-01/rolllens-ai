"""Strict parsing boundary for provider responses."""
from typing import Any
from .base import VoterRecord

def validate_records(payload: Any, expected_page: int | None = None, provenance: str | None = None) -> list[VoterRecord]:
    if not isinstance(payload, list):
        raise ValueError("provider output must be a list of records")
    records = []
    for item in payload:
        record = VoterRecord.model_validate(item)
        if expected_page is not None and record.page_number != expected_page:
            raise ValueError("record page number does not match source page")
        if provenance is not None and record.provenance != provenance:
            raise ValueError("record provenance does not match configured provider")
        for field_name in ("serial_number", "voter_id", "name", "relative_name", "house_number", "age", "gender"):
            field = getattr(record, field_name)
            if field.value is None and field.status == "observed":
                raise ValueError(f"{field_name}: null values must be marked missing or illegible")
            if field.bbox:
                # Pydantic validates ranges; this also validates right/bottom edges.
                from .base import BoundingBox
                BoundingBox.validate_box(field.bbox.model_dump())
        records.append(record)
    return records

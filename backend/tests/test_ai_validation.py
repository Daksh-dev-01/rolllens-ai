import pytest
from app.ai.validation import validate_records
from app.ai.base import PageMetadata
from app.ai.provider import MockProvider

VALID={"serial_number":{"value":1,"status":"observed"},"voter_id":{"value":None,"status":"missing"},"name":{"value":"A","status":"observed"},"relative_name":{"value":None,"status":"missing"},"house_number":{"value":None,"status":"missing"},"age":{"value":42,"status":"observed"},"gender":{"value":"F","status":"observed"},"page_number":1,"provenance":"model","review_status":"unreviewed"}
def test_valid_output(): assert validate_records([VALID],1,"model")[0].name.value == "A"
def test_reject_extra_field():
    with pytest.raises(Exception): validate_records([{**VALID,"sql":"DROP TABLE"}])
def test_reject_bad_bbox():
    bad={**VALID,"name":{"value":"A","status":"observed","bbox":{"x":0.9,"y":0.1,"width":0.2,"height":0.1}}}
    with pytest.raises(Exception): validate_records([bad])
def test_missing_fields_unknown_by_default():
    record=validate_records([{"page_number":1,"provenance":"model"}])[0]
    assert record.name.value is None and record.name.status == "missing"
@pytest.mark.asyncio
async def test_mock_provider_without_credentials():
    records=await MockProvider().extract(b"fixture",PageMetadata(document_id="d",version_id="v",page_number=3))
    assert records[0].provenance == "mock" and records[0].page_number == 3
def test_live_provider_fails_closed_without_credentials(monkeypatch):
    from app.ai.provider import get_provider
    monkeypatch.setenv("ROLLLENS_AI_PROVIDER", "vllm")
    monkeypatch.delenv("ROLLLENS_AI_BASE_URL", raising=False)
    monkeypatch.delenv("ROLLLENS_AI_MODEL", raising=False)
    monkeypatch.delenv("ROLLLENS_AI_API_KEY", raising=False)
    with pytest.raises(RuntimeError): get_provider()

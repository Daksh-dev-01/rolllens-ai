from fastapi.testclient import TestClient
from app.main import app
from app.schemas.records import RecordInput
from pydantic import ValidationError

def test_reject_non_pdf_upload():
    response = TestClient(app).post('/api/v1/documents', files={'file': ('notes.txt', b'hello', 'text/plain')})
    assert response.status_code == 415

def test_reject_invalid_bbox():
    try:
        RecordInput(page_id='page-x', bbox=[0.9, 0.9, 0.5, 0.5])
        assert False, 'expected bbox validation error'
    except ValidationError:
        pass

def test_reject_invalid_age():
    try:
        RecordInput(page_id='page-x', age=150)
        assert False, 'expected age validation error'
    except ValidationError:
        pass

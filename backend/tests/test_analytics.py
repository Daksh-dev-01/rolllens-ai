from fastapi.testclient import TestClient
from app.main import app

def test_analytics():
    body = TestClient(app).get('/api/v1/analytics').json()['data']
    assert body['total_records'] >= 0
    assert body['verified_records'] <= body['total_records']

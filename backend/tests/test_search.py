from fastapi.testclient import TestClient
from app.main import app

def test_search_pagination():
    c = TestClient(app)
    response = c.get('/api/v1/records', params={'page':1,'page_size':2})
    assert response.status_code == 200
    body = response.json()['data']
    assert len(body['items']) <= 2
    assert body['total'] >= len(body['items'])

def test_invalid_age_range():
    response = TestClient(app).get('/api/v1/records', params={'min_age':50,'max_age':10})
    assert response.status_code == 422

import pytest
from app import app  # Import your Flask app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_time(client):
    response = client.get('/time')
    assert response.status_code == 200
    json_data = response.get_json()
    assert "current_time" in json_data
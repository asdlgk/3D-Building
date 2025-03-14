import pytest
import io
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_valid_upload(client):
    test_file = (io.BytesIO(b'fake image data'), 'test.jpg')
    response = client.post(
        '/api/upload',
        data={'image': test_file},
        content_type='multipart/form-data'
    )
    assert response.status_code == 200
    assert 'task_id' in response.json

def test_invalid_file_type(client):
    test_file = (io.BytesIO(b'fake exe data'), 'test.exe')
    response = client.post(
        '/api/upload',
        data={'image': test_file},
        content_type='multipart/form-data'
    )
    assert response.status_code == 415

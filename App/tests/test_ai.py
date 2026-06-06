from fastapi.testclient import TestClient

from App.main import app
from App import data

client = TestClient(app)


def test_ai_without_dataset():

    data.current_df = None

    response = client.post(
        "/ai/ask",
        json={
            "question": "Vilken bil är dyrast?"
        }
    )

    assert response.status_code == 200
    assert response.json() == {
        "error": "No dataset uploaded"
    }
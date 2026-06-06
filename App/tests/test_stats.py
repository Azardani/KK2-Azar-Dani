from fastapi.testclient import TestClient

from App.main import app
from App import data

client = TestClient(app)


def test_stats_without_dataset():

    data.current_df = None
    response = client.get("/data/stats")
    assert response.status_code == 200
    assert response.json() == {
        "error": "No dataset uploaded"
    }
from fastapi.testclient import TestClient

from App.main import app

client = TestClient(app)


def test_upload_wrong_file_type():

    response = client.post(
        "/data/upload",
        files={
            "file": (
                "test.txt",
                b"hello world",
                "text/plain"
            )
        }
    )

    assert response.status_code == 200
    assert response.json() == {
        "error": "Only CSV files are allowed"
    }
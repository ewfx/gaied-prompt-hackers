from fastapi.testclient import TestClient
import pytest
import json
from src.main import app

client = TestClient(app)

@pytest.fixture
def sample_rules():
    return {
        "urgent": ["urgent", "asap", "emergency"],
        "spam": ["buy now", "limited offer", "discount"],
        "personal": ["family", "holiday", "birthday"]
    }

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_upload_rules(sample_rules):
    response = client.post(
        "/upload-rules",
        files={"file": ("rules.json", json.dumps(sample_rules))}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "Rules uploaded successfully"

def test_classify_email():
    # First upload rules
    rules = {"urgent": ["urgent", "asap"]}
    client.post(
        "/upload-rules",
        files={"file": ("rules.json", json.dumps(rules))}
    )
    
    # Then test email classification
    email_content = "This is an URGENT message!"
    response = client.post(
        "/upload-email",
        files={"file": ("email.txt", email_content)}
    )
    assert response.status_code == 200
    assert "urgent" in response.json()["categories"]

def test_classify_uncategorized_email():
    email_content = "This is a regular message"
    response = client.post(
        "/upload-email",
        files={"file": ("email.txt", email_content)}
    )
    assert response.status_code == 200
    assert "uncategorized" in response.json()["categories"]

from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_github_webhook_low_risk():
    payload = {
        "repository": {"full_name": "owner/repo"},
        "pusher": {"name": "dev1"},
        "commits": [
            {
                "added": ["src/main.py"],
                "modified": ["README.md"],
                "removed": []
            }
        ]
    }
    response = client.post("/webhook/github", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["repo"] == "owner/repo"
    assert data["risk_level"] == "LOW"
    assert "Proceed" in data["recommendation"]

def test_github_webhook_high_risk():
    # Large number of sensitive files and high line count
    payload = {
        "repository": {"full_name": "owner/critical-service"},
        "pusher": {"name": "admin"},
        "total_lines_changed": 1000,
        "commits": [
            {
                "added": ["infra/terraform/main.tf", "config/settings.yaml", "db/migration.sql"],
                "modified": ["api/auth.py", "security/firewall.rules", "deployment/k8s.yaml"],
                "removed": []
            }
        ]
    }
    response = client.post("/webhook/github", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["risk_score"] > 0.5
    assert data["risk_level"] in ["MEDIUM", "CRITICAL"]

def test_github_webhook_empty_payload():
    payload = {
        "repository": {"full_name": "owner/repo"},
        "commits": []
    }
    response = client.post("/webhook/github", json=payload)
    assert response.status_code == 200
    assert response.json()["message"] == "No commits found in payload"

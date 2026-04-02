from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_github_webhook_critical_risk_triggers_failover():
    """
    Test that a CRITICAL risk level in the commit results in an automated failover trigger.
    """
    payload = {
        "repository": {"full_name": "owner/critical-service"},
        "pusher": {"name": "admin"},
        "total_lines_changed": 1000, # Triggers high-risk score
        "commits": [
            {
                "added": [
                    "infra/terraform/main.tf", 
                    "config/settings.yaml", 
                    "db/migration.sql",
                    "deployment/k8s.yaml",
                    "security/firewall.rules",
                    "infra/vpc.tf",
                    "infra/iam.tf",
                    "infra/s3.tf",
                    "infra/rds.tf",
                    "infra/eks.tf",
                    "infra/alb.tf"
                ],
                "modified": ["api/auth.py"],
                "removed": []
            }
        ]
    }
    response = client.post("/webhook/github", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    # Assertions for automation logic
    assert data["risk_level"] == "CRITICAL"
    assert data["automation_status"] == "FAILOVER_TRIGGERED"
    assert "failover_details" in data
    assert data["failover_details"]["overall_status"] == "COMPLETED"
    
    # Check if all cloud providers are listed in the results
    providers = [result["cloud"] for result in data["failover_details"]["provider_results"]]
    assert "AWS" in providers
    assert "Azure" in providers
    assert "GCP" in providers

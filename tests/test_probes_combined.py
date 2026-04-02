from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_get_combined_cloud_status():
    """
    Tests the aggregated cloud status endpoint.
    Since we don't have real credentials in the test environment,
    we expect the reports to reflect either 'DOWN', 'DEGRADED', or contain error messages,
    but the endpoint itself should respond with 200 OK.
    """
    response = client.get("/cloud-status")
    assert response.status_code == 200
    
    data = response.json()
    assert "timestamp" in data
    assert "providers" in data
    
    providers = data["providers"]
    assert "AWS" in providers
    assert "Azure" in providers
    assert "GCP" in providers
    
    # Check structure of AWS report
    assert "status" in providers["AWS"]
    assert "details" in providers["AWS"]
    
    # Check structure of Azure report
    assert "status" in providers["Azure"]
    assert "details" in providers["Azure"]

def test_get_combined_cloud_status_with_params():
    """
    Tests the endpoint with custom query parameters.
    """
    params = {
        "aws_services": ["s3", "dynamodb"],
        "azure_rg": "test-rg",
        "gcp_project": "test-project"
    }
    # Note: passing lists in query params usually requires multiple keys or specific formatting
    # FastAPI handles ?aws_services=s3&aws_services=dynamodb
    query_string = "aws_services=s3&aws_services=dynamodb&azure_rg=test-rg&gcp_project=test-project"
    response = client.get(f"/cloud-status?{query_string}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["providers"]["AWS"]["details"].get("S3") is not None
    assert data["providers"]["AWS"]["details"].get("DYNAMODB") is not None

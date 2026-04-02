import os
from typing import Dict
from google.cloud import monitoring_v3
from google.api_core import exceptions

def get_gcp_health(project_id: str) -> Dict[str, str]:
    """
    Checks the connectivity and health of the GCP Monitoring API as a proxy for project health.
    Returns a status dictionary.
    
    Expects GOOGLE_APPLICATION_CREDENTIALS environment variable to be set.
    """
    if not project_id:
        return {"error": "GCP_PROJECT_ID not set"}

    health_status = {}
    
    try:
        client = monitoring_v3.MetricServiceClient()
        project_name = f"projects/{project_id}"
        
        # We attempt to list metric descriptors as a lightweight check for API health and connectivity
        # In a real scenario, we would check specific Compute/GKE/Cloud Run metrics.
        metrics = client.list_metric_descriptors(name=project_name, filter='metric.type="compute.googleapis.com/instance/uptime"', page_size=1)
        
        # If we reach here, the API is responsive
        health_status["MonitoringAPI"] = "UP"
        health_status["ComputeEngine"] = "UP" # Placeholder for specific service health
        
    except exceptions.GoogleAPICallError as e:
        return {"error": f"GCP API error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

    return health_status

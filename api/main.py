from fastapi import FastAPI, Query
from api.commit_listener import router as commit_router
from api.failover_manager import router as failover_router
from api.probes import router as probes_router
from api.failover_trigger import trigger_failover # Imported as requested
from cloud_probe.aws_health import get_aws_health
from cloud_probe.azure_health import get_azure_health
from cloud_probe.gcp_health import get_gcp_health
from datetime import datetime
import os

app = FastAPI(title="Commit Reliability Engine V2")

# Include routers for modular endpoints
app.include_router(commit_router, tags=["Webhooks"])
app.include_router(failover_router, tags=["Failover Management"])
app.include_router(probes_router, tags=["Cloud Probes"])

@app.get("/health")
async def health():
    """
    Basic health check for the API service itself.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "v2.0.0"
    }

@app.get("/cloud-status")
async def get_combined_status(
    aws_services: list[str] = Query(default=["ec2", "rds", "lambda"]),
    azure_rg: str = Query(default="default-resource-group"),
    gcp_project: str = Query(default="default-project-id")
):
    """
    Aggregates health status from AWS, Azure, and GCP into a single report.
    """
    # Use environment variables if not provided in query (optional enhancement)
    az_rg = os.getenv("AZURE_RESOURCE_GROUP", azure_rg)
    gcp_id = os.getenv("GCP_PROJECT_ID", gcp_project)

    aws_report = get_aws_health(aws_services)
    azure_report = get_azure_health(az_rg)
    gcp_report = get_gcp_health(gcp_id)

    return {
        "timestamp": datetime.now().isoformat(),
        "summary": "Multi-Cloud Reliability Report",
        "providers": {
            "AWS": {
                "status": "UP" if all(v == "UP" for v in aws_report.values()) else "DEGRADED",
                "details": aws_report
            },
            "Azure": {
                "status": "UP" if "error" not in azure_report and all(v == "UP" for v in azure_report.values() if isinstance(v, str)) else "DEGRADED",
                "details": azure_report
            },
            "GCP": {
                "status": "UP" if "error" not in gcp_report and all(v == "UP" for v in gcp_report.values() if isinstance(v, str)) else "DEGRADED",
                "details": gcp_report
            }
        }
    }

# The POST /webhook/github endpoint is provided via the commit_router

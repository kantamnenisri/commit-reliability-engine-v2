from fastapi import APIRouter, HTTPException, Query
from cloud_probe.aws_health import get_aws_health
from cloud_probe.azure_health import get_azure_health
from cloud_probe.gcp_health import get_gcp_health
from typing import List, Optional

router = APIRouter()

@router.get("/probes/aws/status")
async def get_aws_status(services: Optional[List[str]] = Query(default=["ec2", "rds", "lambda"])):
    """
    Returns the current health status of requested AWS services.
    """
    try:
        status_report = get_aws_health(services)
        return {
            "cloud_provider": "AWS",
            "health_report": status_report
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve AWS health: {str(e)}")

@router.get("/probes/azure/status")
async def get_azure_status(resource_group: str = Query(..., description="Name of the Azure Resource Group to check")):
    """
    Returns the current health status of resources in the specified Azure Resource Group.
    """
    try:
        status_report = get_azure_health(resource_group)
        if "error" in status_report:
            raise HTTPException(status_code=400, detail=status_report["error"])
        return {
            "cloud_provider": "Azure",
            "resource_group": resource_group,
            "health_report": status_report
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve Azure health: {str(e)}")

@router.get("/probes/gcp/status")
async def get_gcp_status(project_id: str = Query(..., description="GCP Project ID to check")):
    """
    Returns the current health status of services in the specified GCP Project.
    """
    try:
        status_report = get_gcp_health(project_id)
        if "error" in status_report:
            raise HTTPException(status_code=400, detail=status_report["error"])
        return {
            "cloud_provider": "GCP",
            "project_id": project_id,
            "health_report": status_report
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve GCP health: {str(e)}")

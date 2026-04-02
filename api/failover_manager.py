from fastapi import APIRouter, HTTPException
from cloud_probe.orchestrator import CloudOrchestrator
from pydantic import BaseModel

router = APIRouter()
orchestrator = CloudOrchestrator()

class FailoverRequest(BaseModel):
    reason: str
    triggered_by: str = "system"

@router.post("/failover/trigger")
async def trigger_failover(request: FailoverRequest):
    """
    Manually or automatically trigger a multi-cloud failover.
    """
    try:
        report = await orchestrator.execute_multi_cloud_failover()
        return {
            "message": "Multi-cloud failover sequence initiated",
            "reason": request.reason,
            "triggered_by": request.triggered_by,
            "report": report
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failover execution failed: {str(e)}")

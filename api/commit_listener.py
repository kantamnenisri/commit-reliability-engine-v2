from fastapi import APIRouter, Request, HTTPException
from ml.reliability_scorer import score_reliability, CommitMetadata
from cloud_probe.orchestrator import CloudOrchestrator
from api.failover_trigger import trigger_failover
from typing import List

router = APIRouter()
orchestrator = CloudOrchestrator()

@router.post("/webhook/github")
async def github_webhook(request: Request):
    """
    Receives GitHub push event, extracts relevant metadata, 
    calculates risk, and triggers proactive failover if score is high.
    """
    payload = await request.json()
    
    try:
        repo_name = payload.get("repository", {}).get("full_name", "unknown")
        commits = payload.get("commits", [])
        
        if not commits:
            return {"message": "No commits found in payload", "risk_score": 0}
            
        author = payload.get("pusher", {}).get("name", "unknown")
        files_changed = []
        commit_message = ""
        
        for commit in commits:
            files_changed.extend(commit.get("added", []))
            files_changed.extend(commit.get("modified", []))
            files_changed.extend(commit.get("removed", []))
            commit_message += commit.get("message", "") + " "
            
        files_changed = list(set(files_changed))
        total_lines = payload.get("total_lines_changed", len(files_changed) * 20) 

        metadata = CommitMetadata(
            repo_name=repo_name,
            author=author,
            files_changed=files_changed,
            lines_changed=total_lines,
            commit_message=commit_message.strip()
        )
        
        risk_score = score_reliability(metadata)
        
        # Risk level determination based on 0-100 scale
        risk_level = "LOW"
        if risk_score > 80:
            risk_level = "CRITICAL"
        elif risk_score > 40:
            risk_level = "MEDIUM"
            
        risk_report = {
            "repo": repo_name,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "recommendation": "Trigger Proactive Failover" if risk_level == "CRITICAL" else "Monitor Closely" if risk_level == "MEDIUM" else "Proceed"
        }
        
        # Automation Logic: Trigger proactive failover if risk is CRITICAL
        if risk_score > 75:
            # Trigger and Log failover for each cloud provider
            trigger_reports = []
            for provider in ["AWS", "Azure", "GCP"]:
                report = trigger_failover(risk_score, provider)
                trigger_reports.append(report)
                
            # Execute actual cloud operations
            failover_report = await orchestrator.execute_multi_cloud_failover()
            
            risk_report["automation_status"] = "FAILOVER_TRIGGERED"
            risk_report["trigger_logs"] = trigger_reports
            risk_report["failover_details"] = failover_report
        else:
            risk_report["automation_status"] = "NO_ACTION_REQUIRED"
            
        return risk_report
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing webhook: {str(e)}")

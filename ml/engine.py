from pydantic import BaseModel
from typing import List, Dict, Any

class CommitData(BaseModel):
    repo_name: str
    author: str
    files_changed: List[str]
    lines_changed: int

def score_reliability(data: CommitData) -> Dict[str, Any]:
    """
    Analyzes commit data to calculate a reliability risk score.
    Heuristics:
    - High number of files changed (>10) increases risk.
    - Large number of lines changed (>500) increases risk.
    - Specific sensitive files (e.g., config, infra) increase risk.
    """
    score = 0.1  # Base risk score
    
    # Impact of file count
    if len(data.files_changed) > 10:
        score += 0.3
    elif len(data.files_changed) > 5:
        score += 0.1
        
    # Impact of lines changed
    if data.lines_changed > 500:
        score += 0.4
    elif data.lines_changed > 100:
        score += 0.2
        
    # Impact of sensitive files
    sensitive_patterns = ['config', 'infra', 'deployment', 'security', 'database']
    for file in data.files_changed:
        if any(pattern in file.lower() for pattern in sensitive_patterns):
            score += 0.1
            break # Only add once for presence of sensitive files
            
    risk_level = "LOW"
    if score > 0.7:
        risk_level = "CRITICAL"
    elif score > 0.4:
        risk_level = "MEDIUM"
        
    return {
        "repo": data.repo_name,
        "risk_score": round(min(score, 1.0), 2),
        "risk_level": risk_level,
        "recommendation": "Trigger Proactive Failover" if risk_level == "CRITICAL" else "Monitor Closely" if risk_level == "MEDIUM" else "Proceed"
    }

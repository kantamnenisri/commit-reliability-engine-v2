from pydantic import BaseModel
from typing import List

class CommitMetadata(BaseModel):
    repo_name: str
    author: str
    files_changed: List[str]
    lines_changed: int
    commit_message: str = ""

def score_reliability(data: CommitMetadata) -> int:
    """
    Calculates a reliability risk score from 0-100 based on commit heuristics.
    Rules:
    - Base score: 10
    - > 20 files changed: +40
    - Changes in /api or /infra: +30
    - Commit message contains 'hotfix' or 'urgent': +20
    """
    score = 10  # Initial baseline
    
    # Rule: More than 20 files changed
    if len(data.files_changed) > 20:
        score += 40
    elif len(data.files_changed) > 10:
        score += 20
        
    # Rule: Changes in /api or /infra folders
    critical_paths = ['api/', '/api', 'infra/', '/infra']
    is_critical_path = any(
        any(path in file for path in critical_paths) 
        for file in data.files_changed
    )
    if is_critical_path:
        score += 30
        
    # Rule: Commit message contains "hotfix" or "urgent"
    urgent_keywords = ['hotfix', 'urgent', 'emergency', 'critical-fix']
    if any(keyword in data.commit_message.lower() for keyword in urgent_keywords):
        score += 20
        
    # Rule: Large line count
    if data.lines_changed > 1000:
        score += 10

    return min(score, 100)

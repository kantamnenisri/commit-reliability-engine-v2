import logging
from datetime import datetime
from typing import Dict, Any

# Configure logging to failover_events.log
logger = logging.getLogger("FailoverTrigger")
logger.setLevel(logging.CRITICAL)

# Create file handler
file_handler = logging.FileHandler("failover_events.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def trigger_failover(risk_score: int, cloud_provider: str) -> Dict[str, Any]:
    """
    Evaluates risk score and triggers a failover alert if threshold is exceeded.
    Logs critical events to failover_events.log.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    action_taken = "NONE"
    
    if risk_score > 75:
        log_message = f"CRITICAL FAILOVER ALERT | Provider: {cloud_provider} | Risk Score: {risk_score} | Status: TRIGGERED"
        logger.critical(log_message)
        action_taken = f"FAILOVER_INITIATED_ON_{cloud_provider.upper()}"
    else:
        action_taken = "MONITORING_ONLY"
        
    return {
        "timestamp": timestamp,
        "cloud_provider": cloud_provider,
        "risk_score": risk_score,
        "action": action_taken,
        "log_file": "failover_events.log"
    }

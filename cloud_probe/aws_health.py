import boto3
import os
from typing import Dict, List
from botocore.exceptions import BotoCoreError, ClientError

def get_aws_health(services: List[str] = ["ec2", "rds", "lambda"]) -> Dict[str, str]:
    """
    Checks the health of specified AWS services by performing minimal API calls.
    Returns a dictionary mapping service names to 'UP' or 'DOWN'.
    
    Expects environment variables:
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - AWS_REGION (default: us-east-1)
    """
    region = os.getenv("AWS_REGION", "us-east-1")
    health_status = {}

    for service in services:
        try:
            if service.lower() == "ec2":
                client = boto3.client("ec2", region_name=region)
                # Simple call to check if the EC2 API is responsive
                client.describe_regions(RegionNames=[region])
                health_status["EC2"] = "UP"
            
            elif service.lower() == "rds":
                client = boto3.client("rds", region_name=region)
                # Check if the RDS API is responsive
                client.describe_db_instances(MaxRecords=20)
                health_status["RDS"] = "UP"
                
            elif service.lower() == "lambda":
                client = boto3.client("lambda", region_name=region)
                # Check if the Lambda API is responsive
                client.list_functions(MaxItems=1)
                health_status["Lambda"] = "UP"
            
            else:
                health_status[service.upper()] = "UNSUPPORTED"

        except (BotoCoreError, ClientError) as e:
            # If it's a credential error, we might want to log it specifically,
            # but for this health check, any service-level failure indicates 'DOWN'
            health_status[service.upper()] = "DOWN"
        except Exception:
            health_status[service.upper()] = "DOWN"

    return health_status

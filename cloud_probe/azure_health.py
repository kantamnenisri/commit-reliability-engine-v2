import os
from typing import Dict, Any
from azure.identity import EnvironmentCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.core.exceptions import AzureError

def get_azure_health(resource_group_name: str) -> Dict[str, str]:
    """
    Checks the health of resources within a specific Azure Resource Group.
    Returns a dictionary mapping resource names to their provisioning state.
    
    Expects environment variables:
    - AZURE_SUBSCRIPTION_ID
    - AZURE_CLIENT_ID
    - AZURE_CLIENT_SECRET
    - AZURE_TENANT_ID
    """
    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
    
    if not subscription_id:
        return {"error": "AZURE_SUBSCRIPTION_ID not set"}

    health_status = {}
    
    try:
        # Use EnvironmentCredential to pick up AZURE_CLIENT_ID, etc.
        credential = EnvironmentCredential()
        resource_client = ResourceManagementClient(credential, subscription_id)
        
        # List resources in the resource group
        resources = resource_client.resources.list_by_resource_group(resource_group_name)
        
        for resource in resources:
            # Note: provisioning_state is a good proxy for health in many cases
            # 'Succeeded' usually means the resource is healthy and running.
            status = resource.provisioning_state if resource.provisioning_state else "UNKNOWN"
            health_status[resource.name] = "UP" if status == "Succeeded" else "DOWN"

        if not health_status:
            return {"message": f"No resources found in resource group {resource_group_name}"}

    except AzureError as e:
        return {"error": f"Azure API error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

    return health_status

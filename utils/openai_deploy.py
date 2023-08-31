

"""This module can be used to deploy a base model with a custom deployment name."""

from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
from azure.identity import AzureCliCredential

def deployment_model_with_custom_name(credential: AzureCliCredential, subscription_id: str,cog_rg: str, openai_instance_name: str, deployment_name: str, model: str, model_version: str)->str:
    """
    This function deploys a specified base Azure OpenAI model to the Azure OpenAI instance with a custom deployment name.
            
    Args: 
        credential (AzureCliCredential): Azure authentication credentials to use
        subscription_id (str): Azure subscription id the Azure OpenAI instance resides
        cog_rg (str): The Cognitive Services Resource Group the Azure OpenAI instance resides
        openai_instance (openai): The Azure OpenAI instance to use
        deployment_name (str): The custom name the deployment should use
        model (str): The Azure OpenAI base model to deploy
        model_version (str): The Azure OpenAI base model version to deploy

    Returns: 
        deployment_id (str): The deployment id to use to interact with the model. Note, deployment_id should be the same as
                            the specified deployment_name
    """    
    
    client = CognitiveServicesManagementClient(credential=credential, subscription_id=subscription_id)

    deployment = client.deployments.begin_create_or_update(
        resource_group_name=cog_rg,
        account_name=openai_instance_name,
        deployment_name=deployment_name,
        content_type = 'application/json',
        deployment={
            "properties": {
            "model": {
                "format": "OpenAI",
                "name": model,
                "version": model_version
            },
            "sku": "standard"
            }
        }
    )
    result = deployment.result()
    print("Deployment Sucessful:")
    print(result)
    deployment_id = result.name

    return deployment_id


# This file is used to generate the completions for the azure openai api

# import openai sdk libraries
import openai

# import python libraries
import re

# import azure sdk libraries
from azure.identity import AzureCliCredential
from azure.core.exceptions import ResourceExistsError

# Import custom libraries
from utils.openai_deploy import deployment_model_with_custom_name
from utils.openai_retry import get_completion

# Main function 
if __name__ == '__main__':
    # Set constants
    API_BASE_URL = ""
    SUBSCRIPTION_ID = ""
    OPENAI_INSTANCE_NAME = ""
    COGNITIVE_SERVICES_RESOURCE_GROUP = ""
 
    # Get access token
    credential = AzureCliCredential()
    access_token = credential.get_token(https://cognitiveservices.azure.com/.default)
 
    # Setup OpenAI SDK
    openai.api_type = "azure_ad"
    openai.api_base = API_BASE_URL
    openai.api_version = "2022-12-01"
    openai.api_key = access_token.token
    
    # Deploy model to use
    subscription_id = SUBSCRIPTION_ID
    model_name = "gpt-35-turbo"
    deployment_name = "gpt-35-turbo"
    model_version = "0613"
    openai_instance_name = OPENAI_INSTANCE_NAME
    cog_rg = COGNITIVE_SERVICES_RESOURCE_GROUP
    
    # Deploy model
    try:
        print(f"Deploying base model, {model_name}, to use")
        deployment_id = deployment_model_with_custom_name(credential = credential, 
                                      subscription_id = subscription_id, 
                                      cog_rg = cog_rg,
                                      openai_instance_name = openai_instance_name,
                                      deployment_name = deployment_name,
                                      model = model_name,
                                      model_version = model_version
                            )

    # If deployment already exists, use existing deployment
    except Exception as exception:
        if isinstance(exception, ResourceExistsError):
            if "Only 1 deployment is allowed for the same model" in exception.exc_msg:
               # Extract existing deployment id
               deployment_id = re.findall(r"'(.*?)'", exception.exc_msg, re.DOTALL)[1]
               print(f"Found existing deployment, {deployment_id}, with same model, {model_name}.")
               print("Using existing model deployment.")
            else:
                print(f"Error deploying model {model_name}")
                raise
        else:
            print(f"Error deploying model {model_name}")
            raise
 
    # Sample prompt to be sent for completion
    completion_prompt = "Write summary of skill sets required to write python code to perform API completions using Azure OpenAI, \
        which includes infrastructure setup as well as prompt engineering"
    
    print(f"Completion prompt: {completion_prompt}")

    # Get completion
    completion_result = get_completion(openai_instance=openai,
                                       deployment_id=deployment_id,
                                       prompt_text=completion_prompt)
 
    print(f"Completion response: {completion_result}")

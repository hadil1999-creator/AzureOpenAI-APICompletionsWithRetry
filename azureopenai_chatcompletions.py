"""
This sample script illustrates how to use the utils.deploy_openai_model.deployment_model_with_custom_name and 
utils.openai_wrapper.get_chatcompletion functions
"""
#from azure.identity import AzureCliCredential
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import ResourceExistsError
import re
import openai
from utils.openai_deploy import deployment_model_with_custom_name
from utils.openai_retry import get_chatcompletion

if __name__ == '__main__':
    # Set constants
    API_BASE_URL = "https://arkr-msft-cogsvc-eus2.openai.azure.com/"
    SUBSCRIPTION_ID = "3e0da524-e2c9-485a-b036-f6584397a0c0"
    OPENAI_INSTANCE_NAME = "arkr-msft-cogsvc-eus2"
    COGNITIVE_SERVICES_RESOURCE_GROUP = "arkr_msft_eastus2"


    # Get access token
#    credential = AzureCliCredential()
    credential = DefaultAzureCredential(exclude_shared_token_cache_credential = True)
    access_token = credential.get_token("https://cognitiveservices.azure.com/.default")

    # Setup OpenAI SDK
    openai.api_type = "azure_ad"
    openai.api_base = API_BASE_URL
    openai.api_version = "2023-03-15-preview"
    openai.api_key = access_token.token
    
    # Deploy model to use
    subscription_id = SUBSCRIPTION_ID
    model_name = "gpt-35-turbo"
    deployment_name = "gpt-35-turbo"
    model_version = "0613"
    openai_instance_name = OPENAI_INSTANCE_NAME
    cog_rg = COGNITIVE_SERVICES_RESOURCE_GROUP
    
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

    # Get Azure OpenAI ChatCompletion
    instructions = "You are an AI assistant that helps people find information."
    messages = [{"role": "system", "content": instructions},{"role":"user","content":"When does summer begin in North America?"}]
    print(f"ChatCompletion: messages: {messages}")

    completion_result = get_chatcompletion(openai_instance=openai,
                                           deployment_id=deployment_id,
                                           message_text=messages)

    print(f"ChatCompletion response: {completion_result}")





"""
This sample script illustrates how to use the utils.openai_deploy.deployment_model_with_custom_name,  
utils.openai_retry.deployment_retrieve and utils.openai_retry.get_chatcompletion functions
""" 
from azure.identity import AzureCliCredential
from azure.core.exceptions import ResourceExistsError
import re
import openai
from utils.openai_deploy import deployment_model_with_custom_name
from utils.openai_retry import get_completion, deployment_retrieve

if __name__ == '__main__':
    # Set constants
    API_BASE_URL = ""
    SUBSCRIPTION_ID = ""
    OPENAI_INSTANCE_NAME = ""
    COGNITIVE_SERVICES_RESOURCE_GROUP = ""

    # Get access token
    credential = AzureCliCredential()
    access_token = credential.get_token("https://cognitiveservices.azure.com/")

    # Setup OpenAI SDK
    openai.api_type = "azure_ad"
    openai.api_base = API_BASE_URL
    openai.api_version = "2022-12-01"
    openai.api_key = access_token.token
    
    # Deploy model to use
    subscription_id = SUBSCRIPTION_ID
    model_name = "gpt-35-turbo"
    deployment_name = "gpt-35-turbo"
    model_version = "0631"
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

    # Retrieve model to use
    print(f"Retrieving base model, {deployment_id}, to use")
    model_id, model_name, model_status = deployment_retrieve(openai_instance=openai, deployment_id=deployment_id)

    if model_status == "succeeded":
        # The model is ready for use
        # Get Azure OpenAI Completion
        print("Testing retrieved model with Completion request")
        text = "Write a product description in bullet points for a renters insurance product that offers customizable coverage,\
        rewards and incentives, flexible payment options and a peer-to-peer referral program. The tone should be persuasive and professional."
        
        print(f"Completion prompt: {text}")
        completion_result = get_completion(openai_instance=openai,
                                       deployment_id=model_id,
                                       prompt_text=text)

        print(f"Completion response: {completion_result}")

    else:
        print(f"Deployed model, deployment id = {model_id} and model name = {model_name} is not in usable state. It is in {model_status} state. To use the model, please wait until model status is 'succeeded'.")



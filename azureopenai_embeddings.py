

"""
This sample script illustrates how to use the utils.deploy_openai_model.deployment_model_with_custom_name and 
utils.openai_wrapper.get_embedding functions
"""
from azure.identity import AzureCliCredential
from azure.core.exceptions import ResourceExistsError
import re
import openai
from utils.openai_deploy import deployment_model_with_custom_name
from utils.openai_retry import get_embedding

if __name__ == '__main__':
    # Set constants
    API_BASE_URL = ""
    SUBSCRIPTION_ID = ""
    OPENAI_INSTANCE_NAME = ""
    COGNITIVE_SERVICES_RESOURCE_GROUP = ""

    # Get access token
    credential = AzureCliCredential()
    access_token = credential.get_token("https://cognitiveservices.azure.com/.default")

    # Setup OpenAI SDK
    openai.api_type = "azure_ad"
    openai.api_base = API_BASE_URL
    openai.api_version = "2022-12-01"
    openai.api_key = access_token.token
    
    # Deploy model to use
    subscription_id = SUBSCRIPTION_ID
    model_name = "text-embedding-ada-002"
    deployment_name = "embeddings_model"
    model_version = "2"
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

    # Get Azure OpenAI Embedding
    text = "Let's encode this text for similarity comparisons!@!"
    print(f"Text to generate embedding: {text}")
    embedding_result = get_embedding(openai_instance=openai,
                                      deployment_id=deployment_id,
                                      input_text=text)

    print(f"Embedding result:\n {embedding_result}")





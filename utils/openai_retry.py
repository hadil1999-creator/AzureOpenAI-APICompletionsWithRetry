# This Script contains the wrapper functions to make Azure OpenAI API calls using retry logic. 
# The retry logic is used to handle the following errors: RateLimitError, ServiceUnavailableError, TryAgain, APIError, Timeout
# The list of errors could be revised based on the errors encountered in production. Certain errors are excluded from retry logic as the outcome of the retry would be the same, for example access denied errors.
# Script covers completions, chat completions, embeddings and deployments.

# import the required libraries
from retry import retry
from typing import Union, List, Any
import openai

# Error codes handled by the retry logic
from openai.error import RateLimitError, ServiceUnavailableError, TryAgain, APIError, Timeout
 
# Default parameters for the retry logic

# The number of times to retry the API call
DEFAULT_TRIES = 4

# The delay between retries
DEFAULT_DELAY = 2  # seconds

# The backoff factor to increase the delay between retries
DEFAULT_BACKOFF = 2

# The maximum delay between retries
DEFAULT_MAX_DELAY = 20  # seconds
 
# OpenAI Completions wrapper
@retry(
        exceptions=(RateLimitError, ServiceUnavailableError, TryAgain, APIError, Timeout),
        tries=DEFAULT_TRIES,
        delay=DEFAULT_DELAY,
        jitter=(0, 2),
        backoff=DEFAULT_BACKOFF,
        max_delay=DEFAULT_MAX_DELAY,
 
)
def get_completion(openai_instance: openai, deployment_id: str, prompt_text: str, **kwargs: Any)->str:
    """
    Completion method for model tuned for text interactions
        
    Args: 
        openai_instance (openai): The Azure OpenAI instance to use
        deployment_id (str): The base model deployment id to use
        prompt_text (str): The text with instructions and/or examples to present to the model
        **kwargs (Any): Azure OpenAI parameters specified for the completion
 
    Returns: 
        completion_text (str): The returned text from Azure OpenAI
    """

    # Call OpenAI Completion API
    response = openai_instance.Completion.create(
            engine=deployment_id,
            prompt=prompt_text,
            **kwargs)
        
    return response.choices[0].text
 
# OpenAI ChatCompletions wrapper
@retry(
        exceptions=(RateLimitError, ServiceUnavailableError, TryAgain, APIError, Timeout),
        tries=DEFAULT_TRIES,
        delay=DEFAULT_DELAY,
        jitter=(0, 2),
        backoff=DEFAULT_BACKOFF,
        max_delay=DEFAULT_MAX_DELAY,
 
)
def get_chatcompletion(openai_instance: openai, deployment_id: str, message_text: List, **kwargs: Any)->str:
    """
    ChatCompletion method for model tuned for chat interactions. 
        
    Args: 
        openai_instance (openai): The Azure OpenAI instance to use
        deployment_id (str): The base model deployment id to use
        message_text (List): The text with the roles, instructions and/or examples to present to the model
        **kwargs (Any): Azure OpenAI parameters specified for the ChatCompletion
 
    Returns: 
        completion_text (str): The returned text from Azure OpenAI
    """
    # Call OpenAI ChatCompletion API
    response = openai_instance.ChatCompletion.create(
            engine=deployment_id,
            messages=message_text,
            **kwargs
            )
 
    return response.choices[0].message["content"]
    
# Embeddings
@retry(
        exceptions=(RateLimitError, ServiceUnavailableError, TryAgain, APIError, Timeout),
        tries=DEFAULT_TRIES,
        delay=DEFAULT_DELAY,
        jitter=(0, 2),
        backoff=DEFAULT_BACKOFF,
        max_delay=DEFAULT_MAX_DELAY,
 
)
def get_embedding(openai_instance: openai, deployment_id: str, input_text: str)->List:
    """
    OpenAI embedding method wrapper with retries
        
    Args: 
        openai_instance (openai): The Azure OpenAI instance to use
        deployment_id (str): The base model deployment id to use
        input_text (str): The text to be presented to the model for the model to generate embedding
 
    Returns: 
        embedding (List): The returned embedding from Azure OpenAI
    """
    response = openai_instance.Embedding.create(deployment_id=deployment_id,
                                     input=input_text)
 
    return response["data"][0]["embedding"]
 
# Deployments - Retrieve deployment
@retry(
        exceptions=(RateLimitError, ServiceUnavailableError, TryAgain, APIError, Timeout),
        tries=DEFAULT_TRIES,
        delay=DEFAULT_DELAY,
        jitter=(0, 2),
        backoff=DEFAULT_BACKOFF,
        max_delay=DEFAULT_MAX_DELAY,
 
)
def deployment_retrieve(openai_instance: openai, deployment_id: str)->Union[str, str, str]:
    """
    OpenAI Deployment.retrieve method wrapper with retries
        
    Args: 
        openai_instance (openai): The Azure OpenAI instance to use
        deployment_id (str): The deployment id of the model to retrieve
        
    Returns: 
        deployment_id (str): The retrieved model deployment id
        model_name (str): The retrieved model name
        model_status (str): The retrieved model status. This is used to determine if the model is in a state so that it can be used.
    """
    model = openai_instance.Deployment.retrieve(deployment_id)
    
    return model.id, model.name, model.status
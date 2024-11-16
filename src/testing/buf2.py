# from gen_ai_hub.proxy.native.openai import completions

# response = completions.create(
#     model_name="meta--llama3.1-70b-instruct",
#     prompt="The Answer to the Ultimate Question of Life, the Universe, and Everything is",
#     max_tokens=20,
#     temperature=0
# )

# print(response)


from gen_ai_hub.proxy.langchain.openai import ChatOpenAI
from gen_ai_hub.proxy.core.proxy_clients import get_proxy_client
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

import json

aic_service_key_path = 'aic_service_key.json'

# Loads the service key file
with open(aic_service_key_path) as ask:
    aic_service_key = json.load(ask)

ai_core_default_key = {
    "client_id": "sb-48170279-1847-417a-b72a-7c870acdad1f!b513065|aicore!b540",
    "client_secret": "960e9eb6-9dc4-4d6f-8c74-ad33899fde6f$Ik_rMCp_lr9XmBnhaduMKmtvkTYHCbmqLYNmHlYeD8E=",
    "auth_url": "https://k-1-sap-synergy-3gb4yjjn.authentication.eu10.hana.ondemand.com/oauth/token",
    "identity_zone": "k-1-sap-synergy-3gb4yjjn",
    "identity_zone_id": "7b3612f9-fa2d-4daf-88d7-1e56bafdbb13",
    "appname": "48170279-1847-417a-b72a-7c870acdad1f!b513065|aicore!b540",
    "base_url": "https://api.ai.prod.eu-central-1.aws.ml.hana.ondemand.com",
    "api_url": "https://api.ai.prod.eu-central-1.aws.ml.hana.ondemand.com"
}

kwargs = {
    "api_url": aic_service_key["serviceurls"]["AI_API_URL"],
    "base_url": aic_service_key["serviceurls"]["AI_API_URL"] + "/v2", # The present AI API version is 2
    "auth_url": aic_service_key["url"] + "/oauth/token",
    "client_id": aic_service_key['clientid'],
    "client_secret": aic_service_key['clientsecret'],
    "resource_group": "",
    "model_name": "gpt-4o-mini"
}

proxy_client_kwargs = {
    
}

# Initialize proxy client
proxy_client = get_proxy_client('gen-ai-hub', **ai_core_default_key)

# Set up the chat model
chat_llm = ChatOpenAI(proxy_model_name='gpt-35-turbo', proxy_client=proxy_client)

# Define the prompt
prompt_template = PromptTemplate(input_variables=["text"], template="Translate to Danish: {text}")

# Create the LLMChain
chain = LLMChain(llm=chat_llm, prompt=prompt_template)

# Run the chain with the input text
response = chain.invoke("Guten Morgen")

# Print the output
print(response)
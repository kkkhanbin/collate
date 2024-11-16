data = [
    ["Test tnvedname", 200, 10],
    ["Another tnvedname", 300, 400],
    ["And another", 90, 1200]
]

ai_core_default_key = {
    "client_id": "sb-48170279-1847-417a-b72a-7c870acdad1f!b513065|aicore!b540",
    "client_secret": "960e9eb6-9dc4-4d6f-8c74-ad33899fde6f$Ik_rMCp_lr9XmBnhaduMKmtvkTYHCbmqLYNmHlYeD8E=",
    "url": "https://k-1-sap-synergy-3gb4yjjn.authentication.eu10.hana.ondemand.com",
    "identity_zone": "k-1-sap-synergy-3gb4yjjn",
    "identity_zone_id": "7b3612f9-fa2d-4daf-88d7-1e56bafdbb13",
    "appname": "48170279-1847-417a-b72a-7c870acdad1f!b513065|aicore!b540",
    "base_url": "https://api.ai.prod.eu-central-1.aws.ml.hana.ondemand.com"
}

import json

import gen_ai_hub.proxy
from gen_ai_hub.proxy.core.proxy_clients import get_proxy_client
proxy_client = get_proxy_client('gen-ai-hub', **ai_core_default_key) # for an AI Core proxy

promptTemplate_fstring = """
You are an SAP HANA Cloud expert.
You are provided multiple context items that are related to the prompt you have to answer.
Use the following pieces of context to answer the question at the end. 
Context:
{context}
Question:
{query}
"""

import gen_ai_hub.proxy.langchain
from langchain.prompts import PromptTemplate
promptTemplate = PromptTemplate.from_template(promptTemplate_fstring)

import tiktoken
from gen_ai_hub.proxy.langchain.openai import ChatOpenAI


import gen_ai_hub


def retrieve_and_query_llm(query: str, metric='COSINE_SIMILARITY', k = 4) -> str:
    context = ''
    context = data

    # Your service key JSON file relative to this notebook
    aic_service_key_path = 'aic_service_key.json'

    # Loads the service key file
    with open(aic_service_key_path) as ask:
        aic_service_key = json.load(ask)

    prompt = promptTemplate.format(query=query, context=' '.join(str(context)))
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(str(prompt)))

    llm = ChatOpenAI(proxy_model_name='gpt-4-32k', max_tokens = 8000)
    
    response = llm.invoke(prompt).content
    print('Query: '+ query)
    print('\nResponse:')
    print(response)


import json


retrieve_and_query_llm("What do you think of namings in the first column?")

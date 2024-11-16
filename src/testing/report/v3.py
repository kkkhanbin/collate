import json

from gen_ai_hub.proxy.langchain.openai import ChatOpenAI

aic_service_key_path = 'aic_service_key.json'

with open(aic_service_key_path) as ask:
    aic_service_key = json.load(ask)

llm = ChatOpenAI(
    aic_service_key["serviceurls"]["AI_API_URL"] + "/v2", # The present AI API version is 2
    auth_url=aic_service_key["url"] + "/oauth/token",
    client_id=aic_service_key['clientid'],
    client_secret=aic_service_key['clientsecret'], 
    proxy_model_name='gpt-4-32k', 
    max_tokens = 8000)

'''
Traceback (most recent call last):
  File "C:\Khanbin\activities\SAP BTP Hackathon 2024\collate-project\src\testing\report\v3.py", line 10, in <module>
    llm = ChatOpenAI(
          ^^^^^^^^^^^
TypeError: ChatOpenAI.__new__() takes 1 positional argument but 2 were given
'''
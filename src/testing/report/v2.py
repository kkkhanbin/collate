import json

from gen_ai_hub.proxy.langchain.openai import ChatOpenAI

aic_service_key_path = 'aic_service_key.json'

with open(aic_service_key_path) as ask:
    aic_service_key = json.load(ask)

llm = ChatOpenAI(
    base_url=aic_service_key["serviceurls"]["AI_API_URL"] + "/v2", # The present AI API version is 2
    auth_url=aic_service_key["url"] + "/oauth/token",
    client_id=aic_service_key['clientid'],
    client_secret=aic_service_key['clientsecret'], 
    proxy_model_name='gpt-4-32k', 
    max_tokens = 8000)

'''
Traceback (most recent call last):
  File "C:\Khanbin\activities\SAP BTP Hackathon 2024\collate-project\src\testing\report\v1.py", line 10, in <module>
    llm = ChatOpenAI(
          ^^^^^^^^^^^
  File "c:\Khanbin\activities\SAP BTP Hackathon 2024\collate-project\.venv\Lib\site-packages\gen_ai_hub\proxy\langchain\openai.py", line 73, in __init__
    super().__init__(*args, openai_api_key='???', **kwargs)
  File "c:\Khanbin\activities\SAP BTP Hackathon 2024\collate-project\.venv\Lib\site-packages\langchain_core\load\serializable.py", line 113, in __init__
    super().__init__(*args, **kwargs)
  File "c:\Khanbin\activities\SAP BTP Hackathon 2024\collate-project\.venv\Lib\site-packages\pydantic\v1\main.py", line 341, in __init__
    raise validation_error
pydantic.v1.error_wrappers.ValidationError: 1 validation error for ChatOpenAI
__root__
  AICoreV2Client.__init__() missing 1 required positional argument: 'base_url' (type=type_error)
'''
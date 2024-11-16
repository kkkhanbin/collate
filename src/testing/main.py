from pprint import pprint

import requests

from ai_core_sdk.ai_core_v2_client import AICoreV2Client
from gen_ai_hub import orchestration

import json

# Your service key JSON file relative to this notebook
aic_service_key_path = 'aic_service_key.json'

# Loads the service key file
with open(aic_service_key_path) as ask:
    aic_service_key = json.load(ask)

base_url = aic_service_key["serviceurls"]["AI_API_URL"] + "/v2"

# Creating an AI API client instance
aicore_client = AICoreV2Client(
    base_url = aic_service_key["serviceurls"]["AI_API_URL"] + "/v2", # The present AI API version is 2
    auth_url=  aic_service_key["url"] + "/oauth/token",
    client_id = aic_service_key['clientid'],
    client_secret = aic_service_key['clientsecret']
)

token = aicore_client.rest_client.get_token()
headers = {
        "Authorization": token,
        'ai-resource-group': "default",
        "Content-Type": "application/json"}

deployment_id = "df9aa73694b6250f"

# Ответ должен включать в себя только Да или нет и если да, то сами комбинации без никаких дополнительных слов. \

body = {
      "messages": [
       {
          "role": "user",
          "content": "У тебя есть группа чисел: [19, 10] и вторая группа: [9, 3, 4, 6, 11]. \
Числа разделены запятыми. Можно брать только те числа, которые разделены запятыми. Брать числа не из двух данных списков нельзя. \
Сумма чисел во второй группе может быть больше, чем в первой могут остаться лишние числа \
Проверь, возможно ли скомбинировать числа из второй группы так, чтобы в сумме каждая комбинация \
была равна каждому числу из первой группы. Один экземпляр числа из второй группы может быть сопоставлен лишь к числу из первой группы лишь один раз, это важно. \
Напиши комбинации если это возможно сделать или нет если невозможно \
"
       },
       {
          "role": "system",
          "content": "You know only about SAP."
       }
      ]
}

# Check deployment status before inference request
deployment_url = "https://api.ai.prod.eu-central-1.aws.ml.hana.ondemand.com/v2/inference/deployments/df9aa73694b6250f/chat/completions?api-version=2023-05-15"
response = requests.post(url=deployment_url, headers=headers, json=body)

pprint(response, width=200)
resp = response.json() 
pprint(resp, width=200)
# status = resp['status']

# deployment_log_url = f"{base_url}/deployments/{deployment_id}/logs"
# if status == "RUNNING":
#         print(f"Deployment-{deployment_id} is running. Ready for inference request")
# else:
#         print(f"Deployment-{deployment_id} status: {status}. Not yet ready for inference request")
#         #retrieve deployment logs
#         #{{apiurl}}/v2/lm/deployments/{{deploymentid}}/logs.

#         response = requests.get(deployment_log_url, headers=headers)
#         print('Deployment Logs:\n', response.text)

# model = "gpt-4o"
# deployment = aicore_client.deployment.get(deployment_id)
# inference_base_url = f"{deployment.deployment_url}/v2" 

# endpoint = f"{inference_base_url}/api/pull"
# print(endpoint)

# #let's pull the target model from ollama
# json_data = {"name": model}

# response = requests.post(endpoint, headers=headers, json=json_data)
# print('Result:', response.text)

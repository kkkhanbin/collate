import requests
import json

from ai_core_sdk.ai_core_v2_client import AICoreV2Client


class AI():
    def __init__(self) -> None:
        aic_service_key_path = 'src/data/aic_service_key.json'
        with open(aic_service_key_path) as ask:
            self.aic_service_key = json.load(ask)

        self.client = AICoreV2Client(
            base_url = self.aic_service_key["serviceurls"]["AI_API_URL"] + "/v2", # The present AI API version is 2
            auth_url=  self.aic_service_key["url"] + "/oauth/token",
            client_id = self.aic_service_key['clientid'],
            client_secret = self.aic_service_key['clientsecret']
        )
        self.token = self.client.rest_client.get_token()

    def ask(self, msg: str):
        # base_url = aic_service_key["serviceurls"]["AI_API_URL"] + "/v2"
        # deployment_id = "df9aa73694b6250f"

        headers = {
                "Authorization": self.token,
                'ai-resource-group': "default",
                "Content-Type": "application/json"}

        deployment_url = "https://api.ai.prod.eu-central-1.aws.ml.hana.ondemand.com/v2/inference/deployments/df9aa73694b6250f/chat/completions?api-version=2023-05-15"

        body = {
            "messages": [{
                "role": "user",
                "content": msg
            }]
        }

        response = requests.post(url=deployment_url, headers=headers, json=body)
        return response


# pprint(response, width=200)
# resp = response.json() 
# pprint(resp, width=200)
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

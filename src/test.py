# import os
# import sys
# sys.path.append(os.path.abspath('..'))

# from pprint import pprint

# from compare import Compare

# test_data = [

#     # 0 Пример номер 2 - Все успешно
#     {
#         "invoices": [
#             [3917400009, 80, 2098.210000, "EIJ11676249", 796, 12, 188000, 167857.140000],
#             [3917400009, 70, 625, "EIJ11676253", 796, 12, 164500, 146875],
#             [3917400009, 130, 1250, "EIJ11676254", 796, 12, 305500, 272767.860000],
#         ],
#         "pos": [
#             ["PO11000741083", 1, 18800.000000, 8, 2350, "шт", "2517102000", "РПРезЭСФ"],
#             ["PO11000741083", 2, 94000.000000, 40, 2350, "шт", "2517102000", "РПРезЭСФ"],
#             ["PO11000741083", 3, 51700.000000, 22, 2350, "шт", "2517102000", "РПРезЭСФ"],
#             ["PO11000741083", 4, 94000.000000, 130, 1400, "шт", "2517102000", "РПРезЭСФ"],
#             ["PO11000741083", 5, 94000.000000, 70, 700, "шт", "2517102000", "РПРезЭСФ"],
#             ["PO11000741083", 5, 94000.000000, 33, 2350, "шт", "2517102000", "РПРезЭСФ"],
#             ["PO11000741083", 5, 94000.000000, 31, 2350, "шт", "2517102000", "РПРезЭСФ"],
#             ["PO11000741083", 5, 94000.000000, 29, 2350, "шт", "2517102000", "РПРезЭСФ"],
#             ["PO11000741083", 6, 305500.000000, 80, 2350, "шт", "2517102000", "РПРезЭСФ"],
#         ]
#     },

#     # 1 Ошибочная номенклатура в обоих документах
#     {
#         "invoices": [
#             [3917400009, 80, 2098.210000, "EIJ11676249", 796, 12, 188000, 167857.140000],
#             [3917400009, 70, 2098.210000, "EIJ11676253", 796, 12, 164500, 146875],
#             [3917400009, 130, 2098.210000, "EIJ11676254", 797, 12, 305500, 272767.860000], # Здесь
#         ],
#         "pos": [
#             ["PO11000741083", 1, 18800.000000, 8, 2350, "шт", "2517102000", "РПРезЭСФ"],
#             ["PO11000741083", 2, 94000.000000, 40, 2350, "шт1", "2517102000", "РПРезЭСФ"], # И здесь
#             ["PO11000741083", 3, 51700.000000, 22, 2350, "шт", "2517102000", "РПРезЭСФ"],
#             ["PO11000741083", 4, 94000.000000, 40, 2350, "шт", "2517102000", "РПРезЭСФ"],
#             ["PO11000741083", 5, 94000.000000, 40, 2350, "шт", "2517102000", "РПРезЭСФ"],
#             ["PO11000741083", 6, 305500.000000, 130, 2350, "шт", "2517102000", "РПРезЭСФ"],
#         ]
#     },

#     # 2 Изменены quantity
#     {
#         "invoices": [
#             [3917400009, 80, 2098.210000, "EIJ11676249", 796, 12, 188000, 167857.140000],
#             [3917400009, 15, 2098.210000, "EIJ11676253", 796, 12, 164500, 146875],
#             [3917400009, 130, 2098.210000, "EIJ11676254", 796, 12, 305500, 272767.860000],
#         ],
#         "pos": [
#             ["PO11000741083", 1, 18800.000000, 8, 2350, "шт", "2517102000", "РПРезЭСФ"],
#             ["PO11000741083", 2, 94000.000000, 23, 2350, "шт", "2517102000", "РПРезЭСФ"],
#             ["PO11000741083", 3, 51700.000000, 12, 2350, "шт", "2517102000", "РПРезЭСФ"],
#             ["PO11000741083", 4, 94000.000000, 40, 2350, "шт", "2517102000", "РПРезЭСФ"],
#             ["PO11000741083", 5, 94000.000000, 50, 2350, "шт", "2517102000", "РПРезЭСФ"],
#             ["PO11000741083", 6, 305500.000000, 130, 2350, "шт", "2517102000", "РПРезЭСФ"],
#             # ["PO11000741083", 7, 305500.000000, 10, 2350, "шт", "2517102000", "РПРезЭСФ"],
#         ]
#     },

#     # 3 Тестовая площадка
#     {
#         "invoices": [
#             [3917400009, 80, 2098.210000, "EIJ11676249", 796, 12, 188000, 167857.140000],
#             [3917400009, 70, 2098.210000, "EIJ11676253", 796, 12, 164500, 146875],
#             [3917400009, 130, 2098.210000, "EIJ11676254", 796, 12, 305500, 272767.860000],

#             [3917400009, 15, 693.75, "EIJ11676255", 6, 12, 305500, 272767.860000],
#             [3917400009, 45, 693.75, "EIJ11676257", 6, 12, 305500, 272767.860000],

#         ],
#         "pos": [
#             ["PO11000741083", 1, 18800.000000, 8, 2350, "шт", "2517102000", "РПРезЭСФ"],
#             ["PO11000741083", 2, 94000.000000, 40, 2350, "шт", "2517102000", "РПРезЭСФ"],
#             ["PO11000741083", 3, 51700.000000, 22, 2350, "шт", "2517102000", "РПРезЭСФ"],
#             ["PO11000741083", 4, 94000.000000, 40, 2350, "шт", "2517102000", "РПРезЭСФ"],
#             ["PO11000741083", 5, 94000.000000, 40, 2350, "шт", "2517102000", "РПРезЭСФ"],
#             ["PO11000741083", 6, 305500.000000, 130, 2350, "шт", "2517102000", "РПРезЭСФ"],

#             ["PO11000741083", 7, 0, 5, 777, "м", "2517102000", "РПРезЭСФ"],
#             ["PO11000741083", 8, 0, 15, 777, "м", "2517102000", "РПРезЭСФ"],
#             ["PO11000741083", 8, 0, 10, 777, "м", "2517102000", "РПРезЭСФ"],
#             ["PO11000741083", 8, 0, 8, 777, "м", "2517102000", "РПРезЭСФ"],
#             ["PO11000741083", 8, 0, 22, 777, "м", "2517102000", "РПРезЭСФ"],
#             ["PO11000741083", 9, 0, 30, 777, "м", "2517102000", "РПРезЭСФ"],
#             ["PO11000741083", 9, 0, 45, 777, "м", "2517102000", "РПРезЭСФ"],
#         ]
#     },
# ]


# def main():
#     cmp = Compare(**test_data[0])
#     resp = cmp.process()
    
#     pprint(resp, width=200)



# if __name__ == "__main__":
#     main()


import requests
import json

from ai_core_sdk.ai_core_v2_client import AICoreV2Client


class AI():
    def __init__(self) -> None:
        aic_service_key_path = 'src/testing/aic_service_key.json'
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


client = AI()
print(client.ask(
    '''Это - два списка наименований товаров: 
['Красная ручка большая', 'Покупка техники для отгрузки'],
['Скупка машин больших', 'Ручка синяя', 'Большая машина']. 
Сопоставь эти наименования между собой один к одному и выведи ответ в виде списка на языке python. 
Ты имеешь право оставить некоторые элементы без пары если думаешь, что у них нет пары
''').json()["choices"][0]["message"]["content"])

import json
import time
import base64
import requests
from gigachat import GigaChat
import os

KAND_API_KEY = os.environ.get("GIGACHAT_API_KEY")
KAND_SECRET_KEY = os.environ.get("GIGACHAT_SECRET")
GIGACHAT_AUTH_TOKEN = os.environ.get("GIGACHAT_AUTH_TOKEN")

model = GigaChat(
    credentials=GIGACHAT_AUTH_TOKEN,
    scope="GIGACHAT_API_PERS",
    model="GigaChat",
    ca_bundle_file="app/cert/russian_trusted_root_ca.cer",
)


class Text2ImageAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            "X-Key": f"Key {api_key}",
            "X-Secret": f"Secret {secret_key}",
        }

    def get_model(self):
        response = requests.get(
            self.URL + "key/api/v1/models", headers=self.AUTH_HEADERS
        )
        data = response.json()
        return data[0]["id"]

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "censored": False,
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {"query": f"{prompt}"},
        }

        data = {
            "model_id": (None, model),
            "params": (None, json.dumps(params), "application/json"),
        }
        response = requests.post(
            self.URL + "key/api/v1/text2image/run",
            headers=self.AUTH_HEADERS,
            files=data,
        )
        data = response.json()
        return data["uuid"]

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(
                self.URL + "key/api/v1/text2image/status/" + request_id,
                headers=self.AUTH_HEADERS,
            )
            data = response.json()
            if data["status"] == "DONE":
                print("Картинка создана")
                return data["images"]

            attempts -= 1
            time.sleep(delay)


def convert2img(user_id, image):
    with open(f"public\\{user_id}.bin", "wb") as f:
        f.write(bytes(image, "UTF-8"))

    f = open(f"public\\{user_id}.bin", "rb")
    byte = f.read()
    f.close()

    decode = open(f"public\\{user_id}.webp", "wb")
    decode.write(base64.b64decode(byte))
    decode.close()
    print("Картинка готова к отправке")

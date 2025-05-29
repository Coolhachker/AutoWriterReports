import aiohttp
import requests

from src.Configs import \
    headers_for_get_api_key, \
    url_for_get_models, \
    url_for_get_api_key, \
    payload, headers_for_auth_requests, \
    url_for_post_message_into_gigachat, json_data_to_post_message_into_gigachat
from src.Configs.Exceptions import InvalidAuthToken, AuthError, NotFoundModel


class EngineOfGigaChatInterface:
    def __init__(self, session: requests.Session):
        self.session = session
        self.api_key: str = ''

    def post_message_into_gigachat(self, message: str):
        json_data = json_data_to_post_message_into_gigachat.copy()
        json_data['messages'][0]['content'] = json_data['messages'][0]['content'] + message

        headers = headers_for_auth_requests.copy()
        headers['Authorization'] = headers['Authorization'] + self.api_key

        with requests.post(
                url_for_post_message_into_gigachat,
                headers=headers,
                json=json_data,
                verify=False) as response:
            if response.status_code == 200:
                response_json = response.json()
                return response_json['choices'][0]['message']['content']
            elif response.status_code == 401:
                raise AuthError('Auth токен невалидный. Продолжение системы невозможно.')
            elif response.status_code == 404:
                raise NotFoundModel('Не найдена модель.')
            else:
                raise Exception(f'Неизвестная ошибка статус код = {response.status_code}')

    def get_model_of_sber(self):
        headers = headers_for_auth_requests.copy()
        headers['Authorization'] = headers['Authorization'] + self.api_key
        with self.session.get(url_for_get_models, headers=headers, verify=False) as response:
            if response.status_code == 200:
                return True
            elif response.status_code == 401:
                raise AuthError('Auth токен невалидный. Продолжение системы невозможно.')

    def get_api_key(self):
        with self.session.post(url_for_get_api_key, data=payload, headers=headers_for_get_api_key, verify=False) as response:
            response_json = response.json()
            if response.status_code == 200:
                self.api_key = response_json['access_token']
            elif response.status_code == 401:
                raise InvalidAuthToken('Auth токен невалидный.')
            elif response.status_code == 400:
                raise AuthError('Auth токен невалидный. Продолжение системы невозможно.')


def set_interface_for_job(session: requests.Session) -> EngineOfGigaChatInterface:
    engine = EngineOfGigaChatInterface(session)
    engine.get_api_key()
    engine.get_model_of_sber()
    return engine
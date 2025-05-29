import base64

import aiohttp
import requests

from src.Configs import \
    headers_for_get_api_key, \
    url_for_get_models, \
    url_for_get_api_key, \
    payload, headers_for_auth_requests
from src.Configs.Exceptions import InvalidAuthToken, AuthError


class EngineOfGigaChatInterface:
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session
        self.api_key: str = ''

    async def post_message_into_gigachat(self):
        async with self.session.post('') as response:
            pass

    async def get_model_of_sber(self):
        headers = headers_for_auth_requests.copy()
        headers['Authorization'] = headers['Authorization'] + self.api_key
        async with self.session.get(url_for_get_models, headers=headers, ssl=False) as response:
            if response.status == 200:
                pass
            elif response.status == 401:
                raise AuthError('Auth токен невалидный. Продолжение системы невозможно.')

    async def get_api_key(self):
        async with self.session.post(url_for_get_api_key, data=payload, headers=headers_for_get_api_key, ssl=False) as response:
            response_json = await response.json()
            if response.status == 200:
                self.api_key = response_json['access_token']
            elif response.status == 401:
                raise InvalidAuthToken('Auth токен невалидный.')
            elif response.status == 400:
                raise AuthError('Auth токен невалидный. Продолжение системы невозможно.')


async def main():
    async with aiohttp.ClientSession() as session:
        engine = EngineOfGigaChatInterface(session)
        await engine.get_api_key()
        await engine.get_model_of_sber()
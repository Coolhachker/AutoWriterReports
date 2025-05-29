import aiohttp

from src.Configs import \
    headers_for_get_api_key, \
    url_for_get_models, \
    url_for_get_api_key, \
    payload, headers_for_auth_requests, \
    url_for_post_message_into_gigachat, json_data_to_post_message_into_gigachat
from src.Configs.Exceptions import InvalidAuthToken, AuthError, NotFoundModel


class EngineOfGigaChatInterface:
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session
        self.api_key: str = ''

    async def post_message_into_gigachat(self):
        json_data = json_data_to_post_message_into_gigachat.copy()
        json_data['messages'][0]['content'] = json_data['messages'][0]['content'] + 'Переходим к компьютеру, который будет выступать исходным для миграции пользовательской среды. Именно с этой установки Windows мы будем переносить данные. Имя этого компьютера - "MIGsource".'

        headers = headers_for_auth_requests.copy()
        headers['Authorization'] = headers['Authorization'] + self.api_key

        async with self.session.post(
                url_for_post_message_into_gigachat,
                headers=headers,
                json=json_data,
                ssl=False) as response:
            if response.status == 200:
                response_json = await response.json()
                return response_json['choices'][0]['message']['content']
            elif response.status == 401:
                raise AuthError('Auth токен невалидный. Продолжение системы невозможно.')
            elif response.status == 404:
                raise NotFoundModel('Не найдена модель.')
            else:
                raise Exception(f'Неизвестная ошибка статус код = {response.status}')

    async def get_model_of_sber(self):
        headers = headers_for_auth_requests.copy()
        headers['Authorization'] = headers['Authorization'] + self.api_key
        async with self.session.get(url_for_get_models, headers=headers, ssl=False) as response:
            if response.status == 200:
                return True
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
        await engine.post_message_into_gigachat()
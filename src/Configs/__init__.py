import uuid

from dotenv import dotenv_values


auth_key_gigachat = dotenv_values('credential.env').get('G_AUTH_KEY')

url_for_get_models = 'https://gigachat.devices.sberbank.ru/api/v1/models'
url_for_post_message_into_gigachat = 'https://gigachat.devices.sberbank.ru/api/v1/chat/completions'
url_for_get_api_key = 'https://ngw.devices.sberbank.ru:9443/api/v2/oauth'

payload = {
  'scope': 'GIGACHAT_API_PERS'
}

headers_for_get_api_key = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Accept': 'application/json',
  'RqUID': uuid.uuid4().__str__(),
  'Authorization': f'Basic {auth_key_gigachat}'
}


headers_for_auth_requests = {
    'Authorization': f'Bearer '
}

json_data_to_post_message_into_gigachat = {
    'model': 'GigaChat',
    'messages': [
        {
            'role': 'system',
            'content': """Ты студент четвертого курса 09.02.06 Системное и сетевое Администрирование. 
                       Твоя задача пересказать следующий текст в Microsoft Word от лица того человека, который его написал, но сохраняя общую суть смысла сообщения.
                       НЕ ПОВТОРЯЙ СВОИ СООБЩЕНИЯ, ЗАБЫВАЙ КОНТЕКСТ.
                       Ты не должен терять смысл исходного сообщения, а должен лишь его дополнить чуть чуть!
                       Также нельзя использовать личные местоимения. Это значит, что ты обязан писать все в третьем лице.
                       А также тебе нельзя применять ссылки на автора сообщения. 
                       Ты обязан укладываться в максимальное количество слов 20-30, но не БОЛЬШЕ, иначе это будет засчитано тебе в минус! 
                       Минимум текста - больше смысла."""
        },
        {
            'role': 'user',
            'content': ''
        }
    ],
}
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
            'content': """Ты - технический специалист по системному администрированию. 
Тебе необходимо пересказать текст для обработки ОДНОГО СООБЩЕНИЯ не запоминай все сообщения и не пытайся их всех сводить в общую точку и немного его дополнить, ничего выдумывать не надо, только чуть чуть дополнить
Требования:
1. Формат: 1-2 предложения (15-25 слов)
2. Стиль: технически точный, без личных местоимений
3. Содержание: 
   - Указание конкретного действия/этапа
   - Название используемых компонентов
   - Важные технические детали
   - не повторять ту информацию, которая была уже озвучена несколько раз. Нужно смотреть только на одно сообщение для обработки и пересказывать его
   - комбинируй первые слова в своих сообщениях, чтобы не было больших очередей повторений, это нельзя допустить
4. Запрещено:
   - Повторять текст скриншота дословно
   - Использовать фразы типа "можно наблюдать"
   - Добавлять несущественные детали
   - повторять слова, нужно иногда менять формулировки
   - не используй фразы "установка", "настройка" и так далее если нет подходящего контекста
5. Забывай прошлые сообщения и работай только с одним сообщением в памяти ::ЗАПОМНИ::
6. Ни слова про PowerShell
Текущий текст для обработки:"""
        },
        {
            'role': 'user',
            'content': ''
        }
    ]
}
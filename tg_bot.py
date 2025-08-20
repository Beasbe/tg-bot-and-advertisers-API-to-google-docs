import requests
import re
from datetime import datetime, timedelta


class ChatAnalyzer:
    def __init__(self, token, chat_id):
        self.api_url = f'https://api.telegram.org/bot{token}/getUpdates'
        self.chat_id = chat_id

    def get_connected_chats(self): # отдает список закрытых ГРУПП к которым подключен бот
        response = requests.get(self.api_url)
        data = response.json()

        chats = {}
        for update in data['result']:
            message = update.get('channel_post')
            if message:
                chat_id = message['chat']['id']
                chat_name = message['chat']['title']
                if chat_id not in chats:
                    chats[chat_id] = chat_name
        return chats

    def get_messages_for_date(self): # забирает сообщения из чата за отпределённую дату, по умолчанию за текущий день
        response = requests.get(self.api_url)
        data = response.json()

        messages = []
        for update in data['result']:
            message = update.get('channel_post')
            if message and message['chat']['id'] == self.chat_id:
                messages.append({
                    'text': message.get('text')
                    })

        return messages

    @staticmethod
    def extract_content(message): # фильтрует ненужные сообщения и выделяет список остановленных рк с каждого сообщения
        if not message.startswith("❌API Останавливаем"):
            return None
        pattern = r"Доставку:(.*)Основание:"
        match = re.search(pattern, message, re.DOTALL)
        if match:
            return match.group(1).split("\n")
        else:
            return None

    def process_messages(self): # инициализируются все функции и пересобирается лист стопов из сообщений
        stops = []
        messages = self.get_messages_for_date()
        for msg in messages:
            stops.append(self.extract_content(msg['text']))

        stops = [x for x in stops if x is not None]
        flattened_list = sum(stops, [])
        cleaned_list = [item for item in flattened_list if item]
        return cleaned_list



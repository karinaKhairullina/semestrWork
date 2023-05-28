import json
from channels.generic.websocket import AsyncWebsocketConsumer
import requests

class FashionNewsConsumer(AsyncWebsocketConsumer):
    """
    Класс, отвечающий за обработку веб-сокет соединения для получения новостей о моде.
    """
    async def connect(self):
        """
        Метод, вызываемый при установлении соединения с веб-сокетом.
        """
        await self.channel_layer.group_add(
            "news_updates",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        """
        Метод, вызываемый при разрыве соединения с веб-сокетом.
        """
        await self.channel_layer.group_discard(
            'fashion_news_group',
            self.channel_name
        )

    async def send_news(self, event):
        """
        Метод для отправки новостей через веб-сокет соединение.
        """
        response = requests.get("https://newsapi.org/v2/everything?q=fashion&apiKey=a320e3ed494e4c4bb0350617c7c30a27")
        message = {
                'type': 'news',
                'articles': response.json()["articles"]
            }

        if response.status_code == 200:
            await self.send(text_data=json.dumps(message))

    async def fashion_news(self, event):
        """
        Метод, обрабатывающий событие получения новостей о моде.
        """
        await self.send(text_data=event['text'])

    async def websocket_disconnect(self, event):
        """
        Метод, вызываемый при разрыве веб-сокет соединения.
        """
        pass

    async def receive(self, text_data=None, bytes_data=None):
        """
        Метод, вызываемый при получении данных от клиента через веб-сокет соединение.
        """
        await self.send_news(self)



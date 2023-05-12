import json
from channels.generic.websocket import AsyncWebsocketConsumer
from fashionShows.views import fashion_news


class FashionNewsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            'fashion_news_group',
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'fashion_news_group',
            self.channel_name
        )

    async def send_news(self, event):
        news = await fashion_news()
        if news:
            message = {
                'type': 'news',
                'articles': news
            }
            await self.send(text_data=json.dumps(message))

    async def fashion_news(self, event):
        await self.send(text_data=event['text'])

    async def websocket_receive(self, event):
        pass

    async def websocket_disconnect(self, event):
        pass

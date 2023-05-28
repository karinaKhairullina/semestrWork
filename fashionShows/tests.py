from channels.testing import WebsocketCommunicator
from fashionShows.consumers import FashionNewsConsumer
from django.test import TestCase, Client


class FashionNewsConsumerTestCase(TestCase):
    async def test_connect(self):
        communicator = WebsocketCommunicator(FashionNewsConsumer.as_asgi(), "/ws/")
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        await communicator.disconnect()

    async def test_send_news(self):
        communicator = WebsocketCommunicator(FashionNewsConsumer.as_asgi(), "/ws/")
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        consumer = FashionNewsConsumer()
        await communicator.send_json_to({
            'type': 'send_news',
        })
        response = await communicator.receive_json_from()
        self.assertEqual(response['type'], 'news')
        self.assertIn('articles', response)
        await communicator.disconnect()

    async def test_disconnect(self):
        communicator = WebsocketCommunicator(FashionNewsConsumer.as_asgi(), "/ws/")
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        await communicator.disconnect()




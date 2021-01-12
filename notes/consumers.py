from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

import json

from . import views


class Request:
    def __init__(self, scope):
        self.user = scope['user']
        self.session = scope['session']


class NoteConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        request = Request(self.scope)
        self.access_link = self.scope['url_route']['kwargs']['name']
        self.note = await sync_to_async(views.retrieve_note)(self.access_link, request.session['author'])
        if self.note == None:
            await self.close()
        self.room_name = 'note_%s' % self.access_link

        print(f'[WS] connect to note: {self.room_name}', flush=True)

        # Join room
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        print(f'[WS] disconnect from note {self.room_name}', flush=True)

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        print(f'[WS] received from note {self.room_name}', flush=True)
        print(f'Data: {text_data}', flush=True)

        context = {
            'message': text_data
        }

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'server_message',
                'message': json.dumps(context)
            }
        )

    # Receive message from room group
    async def server_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

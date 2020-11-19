import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .controllers import *
from .serializers import NoteSerializer


class Request:
    def __init__(self, scope):
        self.user = scope['user']
        self.session = scope['session']


class NoteConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['name']
        self.client = self.scope['url_route']['kwargs']['client']
        if self.room_name != 'blank':
            note = await sync_to_async(note_retrieve)(self.room_name)
            if note:
                self.room_name = note.name
        self.room_group_name = 'note_%s' % self.room_name

        print(f'[WS] connect to room: {self.room_group_name}', flush=True)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        print(f'[WS] disconnect from room {self.room_group_name}', flush=True)

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        print(f'[WS] received from room {self.room_group_name}', flush=True)
        print(f'Data: {text_data}', flush=True)

        payload = json.loads(text_data)
        request = Request(self.scope)

        note = await sync_to_async(note_retrieve)(payload['name'])
        if not note:
            return

        author = await sync_to_async(author_retrieve)(request)
        if not author:
            return

        if author.id != note.author_id:
            if not note.edit or payload['name'] != note.edit_link:
                return

        await sync_to_async(note_update)(note, author, payload)
        serializer = NoteSerializer(note)
        context = {
            'note': serializer.data,
            'source': payload['source'],
            'client': self.client
        }

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
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

from contextvars import Context
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

import json

from . import misc, models


class Request:
    def __init__(self, scope):
        self.user = scope['user']
        self.session = scope['session']


class NoteConsumer(AsyncWebsocketConsumer):
    async def connect(self) -> None:
        request = Request(self.scope)
        self.access_link = self.scope['url_route']['kwargs']['access_link']
        self.client = self.scope['url_route']['kwargs']['client']

        self.note = await sync_to_async(misc.retrieve_note)(self.access_link, request.session['author'])
        if self.note == None:
            await self.close()
            return

        self.note.author = await sync_to_async(models.Author.objects.get)(id=self.note.author_id)
        self.room_note = f'note_{self.note.read_link}'
        self.room_user = f'user_{self.client}'

        # Join room
        await self.channel_layer.group_add(
            self.room_note,
            self.channel_name
        )
        await self.channel_layer.group_add(
            self.room_user,
            self.channel_name
        )

        await self.channel_layer.group_send(
            self.room_user,
            {
                'type': 'server_message',
                'message': await sync_to_async(self.note.serialize)(request.session['author'])
            }
        )

        await self.accept()

    async def disconnect(self, close_code: int) -> None:
        if close_code == 1006:
            return

        request = Request(self.scope)

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_note,
            self.channel_name
        )
        await self.channel_layer.group_discard(
            self.room_user,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data: str) -> None:
        request = Request(self.scope)
        payload = json.loads(text_data)

        self.note = await sync_to_async(misc.update_note)(self.access_link, request.session['author'], payload)
        if self.note is None:
            return
        self.note.author = await sync_to_async(models.Author.objects.get)(id=self.note.author_id)

        context = await sync_to_async(self.note.serialize)('')
        context['client'] = self.client

        if self.note.read:
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_note,
                {
                    'type': 'server_message',
                    'message': context
                }
            )

    # Receive message from room group
    async def server_message(self, event: dict) -> None:
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event['message']))

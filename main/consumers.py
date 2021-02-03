from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

import json

from . import misc


class NoteConsumer(AsyncWebsocketConsumer):
    async def connect(self) -> None:
        self.access_link = self.scope['url_route']['kwargs']['access_link']
        self.client = self.scope['url_route']['kwargs']['client']

        self.note = await sync_to_async(misc.retrieve_note)(self.access_link, self.scope['session']['author'])
        if self.note is None:
            await self.close()
            return

        self.room_note = f'note_{self.note.read_link}'
        self.room_user = f'user_{self.client}'

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
                'message': await sync_to_async(self.note.serialize)(self.scope['session']['author'])
            }
        )

        await self.accept()

    async def disconnect(self, close_code: int) -> None:
        if close_code == 1006:
            return

        source = await sync_to_async(self.note.get_source)()
        if len(source) == 0:
            await sync_to_async(self.note.delete)()

        await self.channel_layer.group_discard(
            self.room_note,
            self.channel_name
        )
        await self.channel_layer.group_discard(
            self.room_user,
            self.channel_name
        )

    async def receive(self, text_data: str) -> None:
        payload = json.loads(text_data)

        await sync_to_async(self.note.update)(
            self.access_link,
            self.scope['session']['author'],
            payload
        )

        context = await sync_to_async(self.note.serialize)('')
        context['client'] = self.client

        if self.note.read:
            await self.channel_layer.group_send(
                self.room_note,
                {
                    'type': 'server_message',
                    'message': context
                }
            )

    async def server_message(self, event: dict) -> None:
        await self.send(text_data=json.dumps(event['message']))

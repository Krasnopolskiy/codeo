import json
import uuid
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .controllers import *
from .serializers import NoteSerializer


class Request:
    def __init__(self, scope):
        self.user = scope['user']
        self.session = scope['session']


class NoteConsumer(WebsocketConsumer):
    def connect(self):
        self.client = uuid.uuid4()
        self.group_name = 'note_%s' % self.scope['url_route']['kwargs']['name']

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave note group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        payload = json.loads(text_data)
        print(payload)
        request = Request(self.scope)

        note = note_retrieve(payload["name"])
        if not note:
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type': 'message',
                    'message': 'not found'
                }
            )
            return

        author = author_retrieve(request)
        if not author:
            author, request = author_create(request)

        if author != note.author and payload["name"] != note.edit_link:
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type': 'message',
                    'message': 'forbidden'
                }
            )
            return

        # Send message to note group
        note_update(note, author, payload)
        serializer = NoteSerializer(note)
        context = {
            'note': serializer.data,
            'source': payload['source'],
            'editor': self.scope['cookies']['csrftoken']
        }
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'message',
                'data': json.dumps(context)
            }
        )

    # Receive message from note group
    def message(self, event):
        message = event['data']

        # Send message to WebSocket
        self.send(text_data=message)

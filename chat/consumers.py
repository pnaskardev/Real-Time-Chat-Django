import json

# we need this to talk to the database
from asgiref.sync import async_to_sync

# consumer or the websocket itself
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # setup the room name
        # we created a new room name for each chat room
        self.room_name=self.scope['url_route']['kwargs']['room_name']

        self.room_group_name= f'chat_{self.room_name}' % self.room_name
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
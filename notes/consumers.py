
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NoteConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.note_id = self.scope['url_route']['kwargs']['note_id']
        self.group_name = f'note_{self.note_id}'

        # Подключаемся к группе Redis
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Метод, который вызывается через Redis, когда кто-то отправляет обновление
    async def like_update(self, event):
        likes = event['likes']
        await self.send(text_data=json.dumps({
            'likes': likes
        }))

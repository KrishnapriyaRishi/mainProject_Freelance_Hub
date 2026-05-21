import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from bookings.models import Booking
from datetime import datetime
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.booking_id = self.scope['url_route']['kwargs']['booking_id']

        self.room_group_name = f'chat_{self.booking_id}'

        user = self.scope["user"]

        # Check permission
        allowed = await self.is_user_allowed(user)

        if not allowed:
            await self.close()
            return

        # Join room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):

        data = json.loads(text_data)

        message = data['message']

        user = self.scope["user"]

        # Save message
        await self.save_message(user, message)

        # Broadcast message
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': user.username,
            }
        )

    async def chat_message(self, event):

        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
        }))




    @sync_to_async
    def save_message(self, user, message):

        booking = Booking.objects.get(id=self.booking_id)

        Message.objects.create(
            booking=booking,
            sender=user,
            message=message
        )




    @sync_to_async
    def is_user_allowed(self, user):

        booking = Booking.objects.get(id=self.booking_id)

        return (
            user == booking.customer or
            user == booking.provider.user
        )
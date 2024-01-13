from rest_framework import serializers
from .models import Chat, Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'req', 'res']
        # extra_kwargs = {
        #     'chat': {'write_only': True}
        # }

class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True)
    class Meta:
        model = Chat
        fields = ['id', 'title', 'messages']
    def create(self, validated_data):
        messages = validated_data.pop('messages')
        req_data = messages[0]['req'].split()
        first_three_words = ' '.join(req_data[:3])
        chat = Chat.objects.create(title=first_three_words)
        for message in messages:
            Message.objects.create(chat=chat, **message)
        return chat
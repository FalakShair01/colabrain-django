from rest_framework import serializers
from .models import Chat, Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'req', 'res', 'created_at']


class ChatCreateSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, write_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'user', 'title', 'created_at', 'messages']

    def create(self, validated_data):
        messages_data = validated_data.pop('messages')[0]
        chat = Chat.objects.create(**validated_data)
        message = Message.objects.create(chat=chat, **messages_data)
        return chat
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        messages = MessageSerializer(instance.messages.all(), many=True).data
        data['messages'] = messages
        return data
    

class ChatReadSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'user', 'title', 'created_at', 'messages']


class AddMessageSerializer(serializers.ModelSerializer):
    chat = serializers.PrimaryKeyRelatedField(queryset=Chat.objects.all())
    class Meta:
        model = Message
        fields = ['id', 'req', 'res', 'created_at', 'chat']


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
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Chat, Message
from .serializers import MessageSerializer, ChatReadSerializer, ChatCreateSerializer, AddMessageSerializer
from rest_framework.views import APIView


class CreateNewChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        message_data = {
            'req': request.data.get('req', None),
            'res': 'This is chatbot response',
        }

        data = {
            'title': 'AI Title',
            'user': request.user.id,
            'messages': [message_data]
        }

        serializer = ChatCreateSerializer(data=data, context={'request': request}) 
        serializer.is_valid(raise_exception=True)
        chat = serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)   


class ListAllChatView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        chats = Chat.objects.filter(user=request.user)
        serializer = ChatReadSerializer(chats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteAllChatsView(APIView):    
    def delete(self, request, *args, **kwargs):
        chats = Chat.objects.filter(user=request.user)
        chats.delete()
        return Response({'Message': 'Successfully Deleted All Chats!'}, status=status.HTTP_204_NO_CONTENT)
    

class DeleteSingleChatView(APIView):
    def delete(self,request, *args, **kwargs):
        chat_id = kwargs['chat_id']
        try: 
            chat = Chat.objects.get(id=chat_id)
        except Chat.DoesNotExist:
            return Response({'Message': 'Chat does not exist'}, status=status.HTTP_404_NOT_FOUND)
        chat.delete()
        return Response({'Message': 'Successfully Deleted Chat!'}, status=status.HTTP_204_NO_CONTENT)


class AddMessage(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        chat_id = request.data.get('chat_id', None)
        try: 
            chat = Chat.objects.get(id=chat_id)
        except Chat.DoesNotExist:
            return Response({'Message': 'Chat does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        req = request.data.get('req', None)
        data = {
            'chat' : chat_id,
            'req': req,
            'res': 'This is chatbot response',
        }
        serializer = AddMessageSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

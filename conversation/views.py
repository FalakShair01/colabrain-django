from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Chat, Message
from .serializers import MessageSerializer, ChatReadSerializer, ChatCreateSerializer, AddMessageSerializer, ChatSerializer
from rest_framework.views import APIView


class CreateNewChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        
        message_data = {
            'req': request.data.get('req', None),
            'res': request.data.get('res', None)
        }
        print(message_data)
        words = message_data['res'].split()

        # # Take the first three words
        first_three_words = ' '.join(words[:3])

        data = {
            'title': f'{first_three_words} ...',
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


class SingleChatView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        try:
            chat = Chat.objects.get(id=id)
        except Chat.DoesNotExist:
            return Response({"Error": "Chat with ID Not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ChatReadSerializer(chat)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteAllChatsView(APIView):    
    def delete(self, request, *args, **kwargs):
        chats = Chat.objects.filter(user=request.user)
        chats.delete()
        return Response({'Message': 'Successfully Deleted All Chats!'}, status=status.HTTP_204_NO_CONTENT)
    

class DeleteSingleChatView(APIView):
    permission_classes = [IsAuthenticated]

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
        res = request.data.get('req', None)
        data = {
            'chat' : chat_id,
            'req': req,
            'res': res,
        }
        serializer = AddMessageSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    



class ChatViewset(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    
    def get_queryset(self):
        return Chat.objects.filter(user=self.request.user)

    
    
class MessageViewset(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
# urls.py
from django.urls import path, include
from .views import ChatViewset, MessageViewset, CreateNewChatView, ListAllChatView, DeleteAllChatsView, AddMessage,DeleteSingleChatView, SingleChatView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('chats', ChatViewset)
router.register('messages', MessageViewset)

urlpatterns = [
    path('chats/create_new/', CreateNewChatView.as_view(), name='create-new-chat'), 
    path('chats/all/', ListAllChatView.as_view(), name='list-all-chat'), 
    path('chats/<int:pk>/', SingleChatView.as_view(), name='get-single-chat'), 
    path('chats/delete_all/', DeleteAllChatsView.as_view(), name='delete-all-chats'), 
    path('chats/delete/<int:chat_id>/', DeleteSingleChatView.as_view(), name='delete-single-chat'), 
    path('chats/add_message/', AddMessage.as_view(), name='add-message'),
    path('', include(router.urls))

]

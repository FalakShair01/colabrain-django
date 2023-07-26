# urls.py
from django.urls import path
from .views import CreateNewChatView, ListAllChatView, DeleteAllChatsView, AddMessage, DeleteSingleChatView

urlpatterns = [
    path('chats/create_new/', CreateNewChatView.as_view(), name='create-new-chat'), # done
    path('chats/all/', ListAllChatView.as_view(), name='list-all-chat'), # done
    path('chats/delete_all/', DeleteAllChatsView.as_view(), name='delete-all-chats'), # done
    path('chats/delete/<int:chat_id>/', DeleteSingleChatView.as_view(), name='delete-single-chat'), # done
    path('chats/add_message/', AddMessage.as_view(), name='add-message'),
]

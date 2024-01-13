from django.urls import path, include
from .views import ChatViewset, MessageViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('chats', ChatViewset)
router.register('messages', MessageViewset)

urlpatterns = [
    path('', include(router.urls))
]
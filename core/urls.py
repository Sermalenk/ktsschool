from django.conf.urls import url
from django.urls import path

from core.views import ChatView, MyLoginView, ChatLoginView, MessageCreateView

urlpatterns = [
    url(r'get$', ChatView.as_view(), name='chat_get'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('pretty_login/', ChatLoginView.as_view(), name='pretty_login'),
    path('message_create/', MessageCreateView.as_view(), name='message_create')
]

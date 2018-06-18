from django.conf.urls import url

from core.views import ChatView

urlpatterns = [
    url(r'get$', ChatView.as_view(), name='chat_get')
]

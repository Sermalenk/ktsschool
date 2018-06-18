from django.utils import timezone
from django.views.generic import TemplateView


class ChatView(TemplateView):
    template_name = 'core/chat.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        messages = [{
            'text': 'Привет!',
            'username': 'Ваня',
            'date': timezone.now()
        }] * 15
        data['messages'] = messages
        return data

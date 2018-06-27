from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.serializers import serialize
from django.http import HttpResponseNotAllowed, HttpResponseBadRequest
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, CreateView

from core.forms import LoginForm, PrettyLoginForm, MessageCreateForm
from core.models import Message


class ChatView(LoginRequiredMixin, TemplateView):
    template_name = 'core/chat.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        last_id = self.request.GET.get('last_id')

        if last_id:
            messages = Message.objects.filter(id__gt=last_id).order_by('-id')[:20]
        else:
            messages = Message.objects.all().order_by('-id')

        data['messages'] = messages
        return data


class MessagesView(LoginRequiredMixin, TemplateView):
    template_name = 'core/messages.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        last_id = self.request.GET.get('last_id')

        if last_id:
            messages = Message.objects.filter(id__gt=last_id).order_by('-id')
        else:
            messages = Message.objects.all().order_by('-id')

        data['messages'] = messages
        return data


class MyLoginView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)

                return redirect(reverse('core:chat_get'))

        return render(request, 'form.html', {'form': form, 'form_action': reverse('core:login')})


class ChatLoginView(LoginView):
    template_name = 'form.html'
    form_class = PrettyLoginForm
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['form_action'] = reverse('core:pretty_login')
        return data

    def get_success_url(self):
        return reverse('core:chat_get')


class MessageCreateView(CreateView):
    form_class = MessageCreateForm

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['post'])

    def get_success_url(self):
        return reverse('core:chat_get')

    def form_valid(self, form):
        super().form_valid(form)
        return JsonResponse({
            'id': self.object.id,
            'text': self.object.text,
            'author': self.object.author.username,
            'time': self.object.date,
            'renderedTemplate': render_to_string(
                'core/message.html',
                {'message': self.object},
                self.request
            )
        })

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_invalid(self, form):
        return HttpResponseBadRequest()

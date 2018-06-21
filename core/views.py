from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotAllowed, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, CreateView

from core.forms import LoginForm, PrettyLoginForm, MessageCreateForm
from core.models import Message


class ChatView(LoginRequiredMixin, TemplateView):
    template_name = 'core/chat.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_invalid(self, form):
        return HttpResponseBadRequest()

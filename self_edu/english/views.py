from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DeleteView
from django_filters.rest_framework import DjangoFilterBackend
from psycopg2 import IntegrityError
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from english.forms import AddWordForm, RegisterUserForm, LoginUserForm
from english.models import Word, UserWord
from english.permissions import IsOwnerOrStaffOrReadOnly
from english.serializers import WordSerializer


class EngHomeView(TemplateView):
    template_name = 'english/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Self-Education project'
        return context


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'english/registration.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registration of a new user'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('home')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'english/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('home')


class EngAddWord(LoginRequiredMixin, CreateView):
    form_class = AddWordForm
    template_name = 'english/add_word.html'
    success_url = reverse_lazy('add_word')
    login_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Addition of a new word'
        return context

    def get_form_kwargs(self):
        # Passing the user ID to the form
        kwargs = super(EngAddWord, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        if not Word.objects.filter(en_word=cleaned_data['en_word']).exists():
            instance = form.save(commit=False)
            instance.save()
            form.save_m2m()
            # Apparently you can only add M2M relationships saves after first saving
            instance.users.add(self.request.user)
        else:
            UserWord.objects.create(word=Word.objects.get(en_word=cleaned_data['en_word']),
                                    user=User.objects.get(username=self.request.user)
                                    )
        return redirect('add_word')


def words_app(request):
    return render(request, 'english/word_list.html', {'title': 'Word list'})


def word_game(request):
    return HttpResponse("Игра в слова")


class WordView(ModelViewSet):
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    filterset_fields = ['en_word']
    search_fields = ['en_word', 'ru_word', 'ru_word_optional']
    ordering_fields = ['en_word', 'already_learn']

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(users=self.request.user)
        return query_set


class EngDelWord(LoginRequiredMixin, DeleteView):
    success_url = reverse_lazy('word_list')


def auth(request):
    return render(request, 'english/oauth.html', {'title': 'Authorization page'})


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

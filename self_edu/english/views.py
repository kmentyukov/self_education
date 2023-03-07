from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render, redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from english.forms import AddWordForm
from english.models import Word
from english.permissions import IsOwnerOrStaffOrReadOnly
from english.serializers import WordSerializer


def index_page(request):
    context = {'title': 'Self-Education project',
               'words': Word.objects.all()
               }
    return render(request, 'english/index.html', context=context)


def registration(request):
    return HttpResponse("Регистрация")


def add_word(request):
    if request.method == 'POST':
        form = AddWordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_word')
    else:
        form = AddWordForm()
    return render(request, 'english/add_word.html', {'form': form, 'title': 'Addition of a new word'})


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
    search_fields = ['en_word', 'ru_word']
    ordering_fields = ['en_word', 'already_learn']

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()


def auth(request):
    return render(request, 'english/oauth.html', {'title': 'Authorization page'})


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

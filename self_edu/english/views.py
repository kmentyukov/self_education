from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from english.models import Word
from english.serializers import WordSerializer


def index_page(request):
    return render(request, 'index.html', {'words': Word.objects.all()})


class WordView(ModelViewSet):
    queryset = Word.objects.all()
    serializer_class = WordSerializer


def words_app(request):
    return render(request, 'main_app.html')


from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from english.models import NewWord
from english.serializers import WordSerializer


def index_page(request):
    return render(request, 'index.html', {'words': NewWord.objects.all()})


class WordView(ModelViewSet):
    queryset = NewWord.objects.all()
    serializer_class = WordSerializer


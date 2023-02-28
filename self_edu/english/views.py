from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from english.models import Word
from english.permissions import IsOwnerOrStaffOrReadOnly
from english.serializers import WordSerializer


def index_page(request):
    return render(request, 'index.html', {'words': Word.objects.all()})


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
    return render(request, 'oauth.html')


def words_app(request):
    return render(request, 'main_app.html')

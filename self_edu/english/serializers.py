from rest_framework.serializers import ModelSerializer

from english.models import Word


class WordSerializer(ModelSerializer):
    class Meta:
        model = Word
        fields = ['en_word', 'ru_word']

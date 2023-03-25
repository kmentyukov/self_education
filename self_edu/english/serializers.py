from rest_framework.fields import HiddenField, CurrentUserDefault
from rest_framework.serializers import ModelSerializer

from english.models import Word


class WordSerializer(ModelSerializer):

    class Meta:
        model = Word
        fields = ['id', 'en_word', 'ru_word', 'ru_word_optional']

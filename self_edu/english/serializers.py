from rest_framework.serializers import ModelSerializer

from english.models import NewWord


class WordSerializer(ModelSerializer):
    class Meta:
        model = NewWord
        fields = ['new_en_word', 'word_translation']
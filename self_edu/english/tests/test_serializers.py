from django.test import TestCase

from english.models import Word
from english.serializers import WordSerializer


class WordSerializerTestCase(TestCase):
    def test_ok(self):
        word_1 = Word.objects.all()
        print(word_1)
        #data = WordSerializer()

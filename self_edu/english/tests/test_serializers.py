from django.test import TestCase

from english.models import Word
from english.serializers import WordSerializer


class WordSerializerTestCase(TestCase):
    def test_ok(self):
        word_1 = Word.objects.create(en_word='test', ru_word='тест')
        word_2 = Word.objects.create(en_word='check', ru_word='проверка')
        data = WordSerializer([word_1, word_2], many=True).data
        expected_data = [
            {
                'en_word': 'test',
                'ru_word': 'тест'
            },
            {
                'en_word': 'check',
                'ru_word': 'проверка'
            }
        ]
        self.assertEqual(expected_data, data)

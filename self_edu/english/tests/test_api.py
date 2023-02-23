from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from english.models import Word
from english.serializers import WordSerializer


class WordsApiTestCase(APITestCase):
    def setUp(self):
        self.word_1 = Word.objects.create(en_word='test', ru_word='тест')
        self.word_2 = Word.objects.create(en_word='check', ru_word='проверка')
        self.word_3 = Word.objects.create(en_word='check', ru_word='проверка test')

    def test_get(self):
        url = reverse('word-list')
        response = self.client.get(url)
        serializer_data = WordSerializer([self.word_1,
                                          self.word_2, self.word_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        url = reverse('word-list')
        response = self.client.get(url, data={'en_word': 'check'})
        serializer_data = WordSerializer([self.word_2, self.word_3], many=True).data
        print(serializer_data)
        print('*' * 10)
        print(response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_search(self):
        url = reverse('word-list')
        response = self.client.get(url, data={'search': 'test'})
        serializer_data = WordSerializer([self.word_1, self.word_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

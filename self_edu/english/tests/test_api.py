import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from english.models import Word
from english.serializers import WordSerializer


class WordsApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.word_1 = Word.objects.create(en_word='test', ru_word='тест',
                                          user=self.user)
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
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_search(self):
        url = reverse('word-list')
        response = self.client.get(url, data={'search': 'test'})
        serializer_data = WordSerializer([self.word_1, self.word_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(3, Word.objects.all().count())
        url = reverse('word-list')
        data = {
            'en_word': 'squid',
            'ru_word': 'кальмар'
        }
        self.client.force_login(self.user)
        response = self.client.post(url, data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Word.objects.all().count())
        self.assertEqual(self.user, Word.objects.last().user)

    def test_update(self):
        url = reverse('word-detail', args=(self.word_1.id,))
        data = {
            'en_word': self.word_1.en_word,
            'ru_word': 'проверка'
        }
        self.client.force_login(self.user)
        response = self.client.put(url, data=json.dumps(data),
                                   content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.word_1.refresh_from_db()
        self.assertEqual('проверка', self.word_1.ru_word)

    def test_update_not_user_login(self):
        self.user2 = User.objects.create(username='test_username2')
        url = reverse('word-detail', args=(self.word_1.id,))
        data = {
            'en_word': self.word_1.en_word,
            'ru_word': 'проверка'
        }
        self.client.force_login(self.user2)
        response = self.client.put(url, data=json.dumps(data),
                                   content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual({'detail': ErrorDetail(string='You do not have permission to perform this action.',
                                                code='permission_denied')}, response.data)
        self.word_1.refresh_from_db()
        self.assertEqual('тест', self.word_1.ru_word)

    def test_update_not_user_login_but_staff(self):
        self.user2 = User.objects.create(username='test_username2', is_staff=True)
        url = reverse('word-detail', args=(self.word_1.id,))
        data = {
            'en_word': self.word_1.en_word,
            'ru_word': 'проверка'
        }
        self.client.force_login(self.user2)
        response = self.client.put(url, data=json.dumps(data),
                                   content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.word_1.refresh_from_db()
        self.assertEqual('проверка', self.word_1.ru_word)

    def test_delete(self):
        self.assertEqual(3, Word.objects.all().count())
        url = reverse('word-detail', args=(self.word_1.id,))
        self.client.force_login(self.user)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, Word.objects.all().count())
        serializer_data = WordSerializer([self.word_2, self.word_3], many=True).data
        self.assertEqual(serializer_data, self.client.get(reverse('word-list')).data)

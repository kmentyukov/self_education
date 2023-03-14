from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Word(models.Model):
    en_word = models.CharField(max_length=50, unique=True, db_index=True, verbose_name='English word')
    ru_word = models.CharField(max_length=50, verbose_name='Russian translation', blank=True)
    ru_word_optional = models.CharField(max_length=50, verbose_name='Additional russian translation', blank=True)
    users = models.ManyToManyField(User, through='UserWord', through_fields=('word', 'user'))

    def __str__(self):
        return f'ID {self.id}: {self.en_word}'

    def get_absolute_url(self):
        return reverse('word-detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Английское слово'
        verbose_name_plural = 'Английские слова'
        ordering = ['en_word']


class UserWord(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, null=False, blank=False, on_delete=models.CASCADE)
    show_num = models.IntegerField(verbose_name='Number of shows', default=0)
    already_learn = models.BooleanField(verbose_name='Learned', default=False)

    class Meta:
        verbose_name = 'Английское слово'
        verbose_name_plural = 'Английские слова'

    def __str__(self):
        return self.word


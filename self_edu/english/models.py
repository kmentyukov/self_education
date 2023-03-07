from django.contrib.auth.models import User
from django.db import models


class Word(models.Model):
    en_word = models.CharField(max_length=50, unique=True, db_index=True, verbose_name='English word')
    ru_word = models.CharField(max_length=50, verbose_name='Russian translation', blank=True)
    ru_word_optional = models.CharField(max_length=50, verbose_name='Additional russian translation', blank=True)
    show_num = models.IntegerField(verbose_name='Number of shows', default=0)
    already_learn = models.BooleanField(verbose_name='Learned', default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'ID {self.id}: {self.en_word}'

    class Meta:
        verbose_name = 'Английское слово'
        verbose_name_plural = 'Английские слова'
        ordering = ['en_word']



from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Word(models.Model):
    en_word = models.CharField(max_length=50, db_index=True, verbose_name='English word')
    ru_word = models.CharField(max_length=50, verbose_name='Russian translation', blank=True)
    ru_word_optional = models.CharField(max_length=50, verbose_name='Additional russian translation', blank=True)
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    show_num = models.IntegerField(verbose_name='Number of shows', default=0)
    already_learn = models.BooleanField(verbose_name='Learned', default=False)

    def __str__(self):
        return f'ID {self.id}: {self.en_word}'

    def get_absolute_url(self):
        return reverse('word-detail', kwargs={'pk': self.pk})

    class Meta:
        unique_together = ['en_word', 'user']
        verbose_name = 'Английское слово'
        verbose_name_plural = 'Английские слова'
        ordering = ['en_word']



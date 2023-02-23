from django.contrib.auth.models import User
from django.db import models


class Word(models.Model):
    en_word = models.CharField(max_length=50)
    ru_word = models.CharField(max_length=50, blank=True)
    ru_word_optional = models.CharField(max_length=50, blank=True)
    show_num = models.IntegerField(default=0)
    already_learn = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'ID {self.id}: {self.en_word}'



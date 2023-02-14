from django.contrib.auth.models import User
from django.db import models


class Word(models.Model):
    en_word = models.CharField(max_length=50)
    ru_word = models.CharField(max_length=50)
    show_num = models.IntegerField(default=0)
    already_learn = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.en_word



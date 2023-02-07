from django.contrib.auth.models import User
from django.db import models


class NewWord(models.Model):
    new_en_word = models.CharField(max_length=50)
    word_translation = models.CharField(max_length=50)
    show_num = models.IntegerField(default=0)
    already_learn = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


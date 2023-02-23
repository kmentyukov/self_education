from django.contrib import admin
from django.contrib.admin import ModelAdmin

from english.models import Word


@admin.register(Word)
class WordAdmin(ModelAdmin):
    pass

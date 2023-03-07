from django.contrib import admin
from django.contrib.admin import ModelAdmin

from english.models import Word


@admin.register(Word)
class WordAdmin(ModelAdmin):
    list_display = ('id', 'en_word', 'ru_word', 'ru_word_optional', 'show_num', 'already_learn')
    list_display_links = ('id', 'en_word', 'ru_word', 'ru_word_optional')
    search_fields = ('en_word', 'ru_word', 'ru_word_optional')
    list_filter = ('already_learn',)

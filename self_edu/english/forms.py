from string import ascii_letters

from django import forms
from django.core.exceptions import ValidationError
from django.forms import TextInput

from .models import Word


class AddWordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ['en_word', 'ru_word', 'ru_word_optional']
        widgets = {
            'en_word': forms.TextInput(attrs={'class': 'form-control'}),
            'ru_word': forms.TextInput(attrs={'class': 'form-control'}),
            'ru_word_optional': forms.TextInput(attrs={'class': 'form-control'})
        }

    def clean_en_word(self):
        en_word = self.cleaned_data['en_word']
        if not en_word.isalpha():
            raise ValidationError('The word must contain only letters')
        if not all(map(lambda c: c in ascii_letters, en_word)):
            raise ValidationError('The word must contain only English letters')

        return en_word.lower()

    def clean_ru_word(self):
        ru_word = self.cleaned_data['ru_word']
        if ru_word:
            if not ru_word.isalpha():
                raise ValidationError('The word must contain only letters')
            if not validation_ru_letters(ru_word):
                raise ValidationError('The word must contain only Russian letters')

        return ru_word.lower()

    def clean_ru_word_optional(self):
        ru_word_optional = self.cleaned_data['ru_word_optional']
        if ru_word_optional:
            if not ru_word_optional.isalpha():
                raise ValidationError('The word must contain only letters')
            if not validation_ru_letters(ru_word_optional):
                raise ValidationError('The word must contain only Russian letters')

        return ru_word_optional.lower()


def validation_ru_letters(word):
    cyrillic_letters = ''.join(map(chr, range(ord('А'), ord('я') + 1))) + 'Ёё'
    return all(map(lambda c: c in cyrillic_letters, word))

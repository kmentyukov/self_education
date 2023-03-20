from string import ascii_letters

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField, CaptchaTextInput
from django.db.models import Q

from .models import Word, UserWord


class CustomCaptchaTextInput(CaptchaTextInput):
    template_name = 'english/captcha_field.html'


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label='E-mail', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(widget=CustomCaptchaTextInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class AddWordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ['en_word', 'ru_word', 'ru_word_optional']
        widgets = {
            'en_word': forms.TextInput(attrs={'class': 'form-control'}),
            'ru_word': forms.TextInput(attrs={'class': 'form-control'}),
            'ru_word_optional': forms.TextInput(attrs={'class': 'form-control'})
        }

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(AddWordForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = self.cleaned_data
        if Word.objects.filter(en_word=cleaned_data['en_word']).exists():
            if UserWord.objects.filter(
                Q(word=Word.objects.get(en_word=cleaned_data['en_word']).pk) &
                Q(user=User.objects.get(username=self.user).pk)
            ).exists():
                raise forms.ValidationError("This word has already been added")

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

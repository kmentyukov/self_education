from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField, CaptchaTextInput
from django.db.models import Q

from .models import Word
from .utils import WordFormMixin


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


class AddWordForm(WordFormMixin, forms.ModelForm):
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
        if 'en_word' in cleaned_data:
            if Word.objects.filter(
                    Q(en_word=cleaned_data['en_word']) &
                    Q(user=self.user)
            ).exists():
                raise forms.ValidationError("Это слово уже было добавлено")


class EditWordForm(WordFormMixin, forms.ModelForm):
    class Meta:
        model = Word
        fields = ['en_word', 'ru_word', 'ru_word_optional']
        widgets = {
            'en_word': forms.TextInput(attrs={'class': 'form-control'}),
            'ru_word': forms.TextInput(attrs={'class': 'form-control'}),
            'ru_word_optional': forms.TextInput(attrs={'class': 'form-control'})
        }

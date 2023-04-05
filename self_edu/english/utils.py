from string import ascii_letters

from django.core.exceptions import ValidationError


def validation_ru_letters(word):
    cyrillic_letters = ''.join(map(chr, range(ord('А'), ord('я') + 1))) + 'Ёё -'
    return all(map(lambda c: c in cyrillic_letters, word))


class WordFormMixin(object):
    def clean_en_word(self):
        en_word = self.cleaned_data['en_word']
        if not all(x.isalpha() or x.isspace() or x == '-' for x in en_word):
            raise ValidationError('Слово должно содержать только буквы')
        if not all(map(lambda c: c in ascii_letters + ' -', en_word)):
            raise ValidationError('Слово должно содержать только английские буквы')

        return en_word.lower()

    def clean_ru_word(self):
        ru_word = self.cleaned_data['ru_word']
        if ru_word:
            if not all(x.isalpha() or x.isspace() or x == '-' for x in ru_word):
                raise ValidationError('Слово должно содержать только буквы')
            if not validation_ru_letters(ru_word):
                raise ValidationError('Слово должно содержать только русские буквы')

        return ru_word.lower()

    def clean_ru_word_optional(self):
        ru_word_optional = self.cleaned_data['ru_word_optional']
        if ru_word_optional:
            if not all(x.isalpha() or x.isspace() or x == '-' for x in ru_word_optional):
                raise ValidationError('Слово должно содержать только буквы')
            if not validation_ru_letters(ru_word_optional):
                raise ValidationError('Слово должно содержать только русские буквы')

        return ru_word_optional.lower()

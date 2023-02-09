from django.shortcuts import render

from english.models import NewWord


def index_page(request):
    return render(request, 'index.html', {'words': NewWord.objects.all()})

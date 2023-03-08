"""self_edu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from rest_framework.routers import SimpleRouter

from english.views import WordView, words_app, auth, pageNotFound, word_game, \
    EngHomeView, EngAddWord, RegisterUser

router = SimpleRouter()

router.register(r'words', WordView)

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', EngHomeView.as_view(), name='home'),
    path('registration/', RegisterUser.as_view(), name='registration'),
    path('add_word/', EngAddWord.as_view(), name='add_word'),
    path('words_list/', words_app, name='word_list'),
    path('word_game/', word_game, name='word_game'),
    url('', include('social_django.urls', namespace='social')),
    path('auth/', auth),
    ]

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns = [
        path('__debug__/', include('debug_toolbar.urls')),
    ] + urlpatterns


handler404 = pageNotFound

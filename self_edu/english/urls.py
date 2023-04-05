from django.conf.urls import url
from django.db import router
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from english.views import auth, pageNotFound, word_game, \
    EngHomeView, EngAddWord, RegisterUser, LoginUser, logout_user, EngEditWord, WordViewSet, EngWordList, EngDelWord

router = SimpleRouter()

router.register(r'words', WordViewSet)

urlpatterns = [
    path('', EngHomeView.as_view(), name='home'),
    path('registration/', RegisterUser.as_view(), name='registration'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('add_word/', EngAddWord.as_view(), name='add_word'),
    path('edit_word/<int:pk>/', EngEditWord.as_view(), name='edit_word'),
    path('words_list/', EngWordList.as_view(), name='word_list'),
    path('del_word/<int:pk>/', EngDelWord.as_view(), name='del_word'),
    # path('words_list/', words_app, name='word_list'),
    path('word_game/', word_game, name='word_game'),
    url('', include('social_django.urls', namespace='social')),
    path('auth/', auth),
    path('captcha/', include('captcha.urls')),
    ]

urlpatterns += router.urls

handler404 = pageNotFound

from django.conf.urls import url

from . import views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^resume$',
        views.resume,
        name='resume'),
    url(r'^leaderboard$',
        views.leaderboard,
        name='leaderboard'),
    url(r'^clues$',
        views.clues,
        name='clues'),
    url(r'^clues/(?P<guess>[ a-zA-Z0-9]+)/(?P<noLeader>toclue)$',
        views.clues,
        name='cluesToClue'),
    url(r'^clues/(?P<guess>[ a-zA-Z0-9]+)/(?P<formSubmit>submit)$',
        views.clues,
        name='cluesSubmit'),
]

from django.conf.urls import url

from . import views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^map$',
        TemplateView.as_view(template_name='egghunt/map.html'),
        name='map'),
    url(r'^mapresult$',
        views.mapresult,
        name='mapresult'),
    url(r'^resume$',
        views.resume,
        name='resume'),
    url(r'^start$',
        views.start,
        name='start'),
    url(r'^leaderboard$',
        views.leaderboard,
        name='leaderboard'),
    url(r'^clues/(?P<observerLatitude>[-+]?[0-9]*\.?[0-9]+)/(?P<observerLongitude>[-+]?[0-9]*\.?[0-9]+)$',
        views.clues,
        name='clues'),
    url(r'^clues/(?P<observerLatitude>[-+]?[0-9]*\.?[0-9]+)/(?P<observerLongitude>[-+]?[0-9]*\.?[0-9]+)/(?P<noLeader>toclue)$',
        views.clues,
        name='cluesToClue'),
    url(r'^clues/(?P<observerLatitude>[-+]?[0-9]*\.?[0-9]+)/(?P<observerLongitude>[-+]?[0-9]*\.?[0-9]+)/(?P<formSubmit>submit)$',
        views.clues,
        name='cluesSubmit'),
]
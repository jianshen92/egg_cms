from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
import views

# API endpoints
urlpatterns = format_suffix_patterns([
    url(r'^stream/twitch/',
        views.TwitchList.as_view(),
        name='twitch-list'),
    url(r'^stream/youtube',
        views.YoutubeList.as_view(),
        name='twitch-list'),

])
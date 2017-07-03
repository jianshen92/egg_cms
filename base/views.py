# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import TwitchChannel, YoutubeChannel
from rest_framework import generics
from serializers import TwitchSerializer, YoutubeSerializer
from django.shortcuts import render

# Create your views here.
class TwitchList(generics.ListAPIView):
    serializer_class = TwitchSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = TwitchChannel.objects.all()
        subscribe = self.request.query_params.get('subscribe', None)
        if subscribe is not None:
            queryset = queryset.filter(subscribe=subscribe)
        return queryset

class YoutubeList(generics.ListAPIView):
    queryset = YoutubeChannel.objects.all()
    serializer_class = YoutubeSerializer
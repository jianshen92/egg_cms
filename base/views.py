# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import TwitchChannel, YoutubeChannel
from rest_framework import generics
from serializers import TwitchSerializer, YoutubeSerializer
from django.shortcuts import render

# Create your views here.
class TwitchList(generics.ListAPIView):
    queryset = TwitchChannel.objects.all()
    serializer_class = TwitchSerializer

class YoutubeList(generics.ListAPIView):
    queryset = YoutubeChannel.objects.all()
    serializer_class = YoutubeSerializer
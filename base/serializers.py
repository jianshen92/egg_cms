from rest_framework import serializers
from models import TwitchChannel, YoutubeChannel

class TwitchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TwitchChannel
        fields = ('channel_title', 'channel_name', 'subscribe')

class YoutubeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = YoutubeChannel
        fields = ('channel_title', 'channel_id', 'subscribe')
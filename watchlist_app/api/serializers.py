from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform

class WatchListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = WatchList
        fields = '__all__'

class StreamPlatformSerializer(serializers.ModelSerializer):

    watchlist = WatchListSerializer(many=True, read_only=True)
    about_length = serializers.SerializerMethodField()

    # watchlist = serializers.StringRelatedField(many=True, read_only=True)
    # watchlist = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    # watchlist = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='movie-details')
    # watchlist = serializers.HyperlinkedIdentityField(many=True, read_only=True, view_name='movie-details')

    class Meta:
        model = StreamPlatform
        fields = '__all__'

    def get_about_length(self, object):
        return len(object.about)
from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform, Review

class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        fields = '__all__'

class WatchListSerializer(serializers.ModelSerializer):

    reviews = ReviewSerializer(many=True, read_only=True)  # Adding Nested Serializers
    # reviews = serializers.StringRelatedField(many=True, read_only=True)  # Adding Nested Serializers

    class Meta:
        model = WatchList
        fields = '__all__'

class StreamPlatformSerializer(serializers.ModelSerializer):

    watchlist = WatchListSerializer(many=True, read_only=True)
    about_length = serializers.SerializerMethodField()

    # watchlist = serializers.StringRelatedField(many=True, read_only=True)
    # watchlist = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    # watchlist = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='movie-details')  # Here, requires context = {"request": request}
    # watchlist = serializers.HyperlinkedIdentityField(many=True, read_only=True, view_name='movie-details') # Here, requires context = {"request": request}

    class Meta:
        model = StreamPlatform
        fields = '__all__'

    def get_about_length(self, object):
        return len(object.about)

from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.api.serializers import (WatchListSerializer, StreamPlatformSerializer, ReviewSerializer)

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class ReviewAV(APIView):

    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReviewSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ReviewDetailAV(APIView):
    
    def get(self, request, rpk):
        try:
            review = Review.objects.get(pk=rpk)
        except Review.DoesNotExist:
            return Response(data={'error_message': f"Review with ID {rpk} not found!"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    
    def put(self, request, rpk):
        try:
            review = Review.objects.get(pk=rpk)
        except Review.DoesNotExist:
            return Response(data={'error_message': f"Review with ID {rpk} not found!"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReviewSerializer(review, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, rpk):
        review = Review.objects.get(pk=rpk) 
        review.delete()
        content = {'message': 'Review was deleted'}
        return Response(content, status=status.HTTP_204_NO_CONTENT)

class StreamPlatformListAV(APIView):

    def get(self, request):
        platforms = StreamPlatform.objects.all()
        # serializer = StreamPlatformSerializer(platforms, many=True, context={'request': request})
        serializer = StreamPlatformSerializer(platforms, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class StreamPlatformDetailAV(APIView):

    def get(self, request, spk):
        try:
            platform = StreamPlatform.objects.get(pk=spk)
        except StreamPlatform.DoesNotExist:
            return Response({'message':f"Platform with ID {spk} doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data)

    def put(self, request, spk):
        platform = StreamPlatform.objects.get(pk=spk)
        serializer = StreamPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, spk):
        platform = StreamPlatform.objects.get(pk=spk) 
        platform.delete()
        content = {'message': 'platform deleted'}
        return Response(content, status=status.HTTP_204_NO_CONTENT)

class WatchListAV(APIView):

    def get(self, request):
        watchlist_items = WatchList.objects.all()
        serializer = WatchListSerializer(watchlist_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class WatchListDetailAV(APIView):

    def get(self, request, pk):
        try:
            watchlist_item = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'message':f"Watch Item with ID {pk} doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(watchlist_item)
        return Response(serializer.data)

    def put(self, request, pk):
        watchlist_item = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(watchlist_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        watchlist_item = WatchList.objects.get(pk=pk) 
        watchlist_item.delete()
        content = {'message': 'Watch Item deleted'}
        return Response(content, status=status.HTTP_204_NO_CONTENT)
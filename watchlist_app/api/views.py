
from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.api.serializers import (WatchListSerializer, StreamPlatformSerializer, ReviewSerializer)

from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication

from watchlist_app.api.permissions import AdminOrReadOnly, ReviewUserOrReadOnly

from django.contrib.auth import login, logout, authenticate
from rest_framework.throttling import UserRateThrottle

from watchlist_app.api.throttling import ReviewCreateThrottle, ReviewListThrottle


### LOGIN 
def my_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
    else:
        # Return an 'invalid login' error message.
        return Response('Invalid User Credentials', status=status.HTTP_401_UNAUTHORIZED)


### CLASS BASED VIEWS - 
class ReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [AdminOrReadOnly]
    permission_classes = [AdminOrReadOnly]
    throttle_classes =[ReviewListThrottle]

class MoviewReviewList(generics.ListCreateAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]
    throttle_classes =[ReviewListThrottle]

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)

        reviewer = self.request.user
        review_qs = Review.objects.filter(watchlist=watchlist)
        review_per_reviewer_qs = review_qs.filter(reviewer=reviewer)

        if review_per_reviewer_qs.exists():
            raise ValidationError('You have already reviewed this movie')
        
        if watchlist.rating_count == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2
       
        watchlist.rating_count += 1
        watchlist.save()
        serializer.save(watchlist=watchlist, reviewer=reviewer)
    
class MoviewReviewDetail(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = [TokenAuthentication]
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)
    
    def get_object(self):
        queryset = self.get_queryset()
        review_id = self.kwargs['rpk']
        return generics.get_object_or_404(queryset=queryset, pk=review_id)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]
    throttle_classes = [UserRateThrottle]

class ReviewCreateGAV(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)

        reviewer = self.request.user
        review_qs = Review.objects.filter(watchlist=watchlist, reviewer=reviewer)

        if review_qs.exists():
            raise ValidationError('You have already reviewed this movie')
        serializer.save(watchlist=watchlist, reviewer=reviewer)

### CLASS BASED VIEWS - Mixins ###

# class ReviewList(mixins.ListModelMixin, 
#                 mixins.CreateModelMixin, 
#                 generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
    
# class ReviewDetail(mixins.RetrieveModelMixin, 
#                 mixins.UpdateModelMixin, mixins.DestroyModelMixin,
#                 generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
    
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
    
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

### CLASS BASED VIEWS - APIVIEW ###

# class ReviewAV(APIView):

#     def get(self, request):
#         reviews = Review.objects.all()
#         serializer = ReviewSerializer(reviews, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = ReviewSerializer(request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# class ReviewDetailAV(APIView):
    
#     def get(self, request, rpk):
#         try:
#             review = Review.objects.get(pk=rpk)
#         except Review.DoesNotExist:
#             return Response(data={'error_message': f"Review with ID {rpk} not found!"}, status=status.HTTP_404_NOT_FOUND)
#         serializer = ReviewSerializer(review)
#         return Response(serializer.data)
    
#     def put(self, request, rpk):
#         try:
#             review = Review.objects.get(pk=rpk)
#         except Review.DoesNotExist:
#             return Response(data={'error_message': f"Review with ID {rpk} not found!"}, status=status.HTTP_404_NOT_FOUND)
#         serializer = ReviewSerializer(review, request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, rpk):
#         review = Review.objects.get(pk=rpk) 
#         review.delete()
#         content = {'message': 'Review was deleted'}
#         return Response(content, status=status.HTTP_204_NO_CONTENT)
    
class StreamPlatformListAV(APIView):

    permission_classes = [AdminOrReadOnly]

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

    permission_classes = [AdminOrReadOnly]

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

    permission_classes = [AdminOrReadOnly]
    throttle_classes = [UserRateThrottle]

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
    
    permission_classes = [AdminOrReadOnly]

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
    
####################################

#### ViewSets & Routers ####
class StreamPlatformVS(viewsets.ViewSet):

    def list(self, request):
        queryset = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        queryset = StreamPlatform.objects.all()
        platform = get_object_or_404(queryset, pk=pk)
        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        platform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(platform, request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        queryset = StreamPlatform.objects.all()
        platform = get_object_or_404(queryset, pk=pk)
        platform.delete()
        content = {'message': 'Platform deleted'}
        return Response(content, status=status.HTTP_204_NO_CONTENT)

#############################
    


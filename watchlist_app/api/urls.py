from django.urls import path, include

from rest_framework.routers import DefaultRouter

# from watchlist_app.api.views import movie_list, movie_details
from watchlist_app.api.views import (WatchListAV, WatchListDetailAV, 
                                     StreamPlatformListAV, StreamPlatformDetailAV,
                                     StreamPlatformVS,
                                    #  ReviewAV, ReviewDetailAV
                                    ReviewList, ReviewDetail,
                                    ReviewCreateGAV,
                                    MoviewReviewList, MoviewReviewDetail)
# ROUTERS 
router = DefaultRouter()
router.register('stream', StreamPlatformVS, basename='streamplatform-vs')


urlpatterns = [
    # Watch List URLs
    path('list/', WatchListAV.as_view(), name='movie-list'),
    path('<int:pk>/', WatchListDetailAV.as_view(), name='movie-details'),
    
    path('<int:pk>/review/', MoviewReviewList.as_view(), name='movie-review-list'), # <int:pk>/review/ Review for Movie
    path('<int:pk>/review/create', ReviewCreateGAV.as_view(), name='create-movie-review'), 
    path('<int:pk>/review/<rpk>', MoviewReviewDetail.as_view(), name='movie-review-details'),

    # Stream URLs
    path('', include(router.urls)),
   
    # path('stream/', StreamPlatformListAV.as_view(), name='platform-list'),
    # path('stream/<int:spk>/', StreamPlatformDetailAV.as_view(), name='platform-details'),

    # Review URLs
    # path('review/', ReviewAV.as_view(), name='review-list'),
    # path('review/<int:rpk>/', ReviewDetailAV.as_view(), name='reiew-details')
    path('review/', ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>/', ReviewDetail.as_view(), name='reiew-details')

]
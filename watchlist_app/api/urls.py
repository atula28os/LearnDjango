from django.urls import path
# from watchlist_app.api.views import movie_list, movie_details
from watchlist_app.api.views import (WatchListAV, WatchListDetailAV, 
                                     StreamPlatformListAV, StreamPlatformDetailAV,
                                    #  ReviewAV, ReviewDetailAV
                                    ReviewList, ReviewDetail,
                                    MoviewReviewList, MoviewReviewDetail)

urlpatterns = [
    # Watch List URLs
    path('list/', WatchListAV.as_view(), name='movie-list'),
    path('<int:pk>/', WatchListDetailAV.as_view(), name='movie-details'),
    
    path('<int:pk>/review/', MoviewReviewList.as_view(), name='movie-review-list'), # <int:pk>/review/ Review for Movie
    path('<int:pk>/review/<rpk>', MoviewReviewDetail.as_view(), name='movie-review-details'),

    # Stream URLs
    path('stream/', StreamPlatformListAV.as_view(), name='platform-list'),
    path('stream/<int:spk>/', StreamPlatformDetailAV.as_view(), name='platform-details'),

    # Review URLs
    # path('review/', ReviewAV.as_view(), name='review-list'),
    # path('review/<int:rpk>/', ReviewDetailAV.as_view(), name='reiew-details')
    path('review/', ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>/', ReviewDetail.as_view(), name='reiew-details')

]
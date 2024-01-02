from django.urls import path
# from watchlist_app.api.views import movie_list, movie_details
from watchlist_app.api.views import (WatchListAV, WatchListDetailAV, 
                                     StreamPlatformListAV, StreamPlatformDetailAV)

urlpatterns = [
    path('list/', WatchListAV.as_view(), name='movie-list'),
    path('<int:pk>/', WatchListDetailAV.as_view(), name='movie-details'),
    path('stream/', StreamPlatformListAV.as_view(), name='platform-list'),
    path('stream/<int:spk>/', StreamPlatformDetailAV.as_view(), name='platform-details'),
]
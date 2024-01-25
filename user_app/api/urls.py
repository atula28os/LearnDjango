from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include
from user_app.api.views import UserRegistration, LogoutUser
from watchlist_app.api.views import WatchListAV

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),
    path('register/', UserRegistration.as_view(), name='register'),
]
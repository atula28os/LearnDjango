from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User

from user_app.api.serializers import RegistrationSerializer
from user_app import models

class UserRegistration(APIView):

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        
        data = {}

        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'registration successfull'
            data['username'] = account.username
            data['email'] = account.email
            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = serializer.errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=data)
    
class LogoutUser(APIView):

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
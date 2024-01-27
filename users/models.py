from django.db import models
from django.contrib.auth.models import User

import uuid

# Create your models here.
class Profile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True, default='dummy')
    email = models.EmailField(max_length=250,blank=True, null=True)
    intro = models.CharField(max_length=50,blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_img = models.ImageField(null=True, blank=True, 
                    default='profiles/user-default.png', upload_to='profiles/')
    social = models.CharField(max_length=250,blank=True, null=True)
    github = models.CharField(max_length=250,blank=True, null=True)
    youtube = models.CharField(max_length=250,blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return str(self.user.username)
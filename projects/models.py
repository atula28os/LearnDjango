from django.db import models
import uuid

from users.models import Profile

# Create your models here.
class Project(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    title = models.CharField(max_length=150)
    featured_image = models.ImageField(null=True, blank=True, default='default.jpg')
    description = models.TextField(null=True, blank=True)
    demo_link = models.CharField(max_length=500, blank=True, null=True)
    source_link = models.CharField(max_length=500, blank=True, null=True)
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return self.title
    

class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'UP VOTE'),
        ('down', 'DOWN VOTE')
    )
    # owner = 
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                        primary_key=True, editable=False)
    
    def __str__(self) -> str:
        return self.value
    

class Tag(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return self.name
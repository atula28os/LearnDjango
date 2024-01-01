import json

from django.shortcuts import render
from django.http import JsonResponse

from .models import Movie

# Create your views here.
def movie_list(request):
    movies = Movie.objects.all()
    payload = {"movies": list(movies.values())}
    return JsonResponse(payload)

def movie_detail(request, pk):
    movie = Movie.objects.get(pk=pk)
    payload = {'name': movie.name, 'description': movie.description, 'active': movie.active}
    return JsonResponse(data=payload)
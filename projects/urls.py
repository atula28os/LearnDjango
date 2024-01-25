from django.urls import path

from projects.views import projects, project, createProject, updateProject, deleteProject


urlpatterns = [
    path('', projects, name='projects'),
    path('project/<str:pk>/', project, name='project'),
    path('newproject/create/', createProject, name='create-project'),
    path('update-project/<str:pk>/', updateProject, name='update-project'),
    path('delete-project/<str:pk>/', deleteProject, name='delete-project')
]

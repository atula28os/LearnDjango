from django.forms import ModelForm

from projects.models import Project

class ProjectForm(ModelForm):
    class Meta:
        model = Project 
        exclude = ['vote_total', 'vote_ratio']
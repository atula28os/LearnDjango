from django.forms import ModelForm, widgets
from django import forms 
from projects.models import Project

class ProjectForm(ModelForm):
    class Meta:
        model = Project 
        exclude = ['vote_total', 'vote_ratio']

        widgets = {
            'tags' : forms.CheckboxSelectMultiple()
        }

    def __init__(self,*args, **kwargs) -> None:
        super(ProjectForm, self).__init__(*args, **kwargs)

        # self.fields['title'].widget.attrs.update({'class': 'input', 'placeholder': 'Add a Title'})
        # self.fields['description'].widget.attrs.update({'class': 'input', 'placeholder': 'Add a Description'})

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input', 'placeholder': 'Add a Description'})
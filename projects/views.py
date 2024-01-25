from django.shortcuts import render, redirect
from django.http import HttpResponse

from projects.models import Project, Review, Tag
from projects.forms import ProjectForm

# Create your views here

def projects(request):

    projects = Project.objects.all()
    return render(request=request, 
                  template_name='projects/project.html', 
                  context={'projects': projects})

def project(request, pk):
    data = None
    project = Project.objects.get(id=pk)
    tags = project.tags.all()
    return render(request=request,
                   template_name='projects/single-project.html', context={'project': project, 'tags': tags})

def createProject(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('projects')
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)



def updateProject(request, pk):

    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(data=request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project', pk=pk)
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


def deleteProject(request, pk):

    project = Project.objects.get(id=pk)
    project.delete()
    return redirect('projects')

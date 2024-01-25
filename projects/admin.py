from django.contrib import admin

from projects.models import Project, Review, Tag

# Register your models here.
admin.site.register(model_or_iterable=Project)
admin.site.register(model_or_iterable=Tag)
admin.site.register(model_or_iterable=Review)
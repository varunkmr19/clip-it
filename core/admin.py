from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Tag)
admin.site.register(models.Collection)
admin.site.register(models.Bookmark)
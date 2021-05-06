from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ManyToManyField


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Collection(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='collection')

    def __str__(self):
        return self.name


class Bookmark(models.Model):
    title = models.CharField(max_length=255)
    url = models.TextField()
    collection = models.ManyToManyField(Collection, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bookmark')

    def __str__(self):
        return self.title


class Shortcut(models.Model):
    title = models.CharField(max_length=255)
    url = models.TextField()
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shortcut')

    def __str__(self):
        return self.title

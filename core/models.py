from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
  pass


class Tag(models.Model):
  name = models.CharField(max_length=255)

  def __str__(self):
    return self.name


class Collection(models.Model):
  name = models.CharField(max_length=255)
  tags = models.ManyToManyField(Tag)
  owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collection')

  def __str__(self):
    return self.name


class Bookmark(models.Model):
  title = models.CharField(max_length=255)
  url = models.TextField()
  collection = models.ManyToManyField(Collection)

  def __str__(self):
    return self.title

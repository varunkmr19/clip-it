from django.db.models import fields
from rest_framework import serializers
from core.models import User, Tag, Collection, Bookmark

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
  class Meta:
    model = Tag
    fields = '__all__'
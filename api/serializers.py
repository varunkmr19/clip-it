import collections
from django.db.models import fields
from rest_framework import serializers
from core.models import Tag, Collection, Bookmark


class TagSerializer(serializers.ModelSerializer):
  class Meta:
    model = Tag
    fields = '__all__'


class CollectionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Collection
    fields = ['name']


class BookMarkSerializer(serializers.ModelSerializer):
  tags = TagSerializer(many=True)
  collection = CollectionSerializer(many=True)
  class Meta:
    model = Bookmark
    fields = ['title', 'url', 'tags', 'collection']
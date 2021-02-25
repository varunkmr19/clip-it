from django.shortcuts import render
from rest_framework import mixins, generics
from . serializers import TagSerializer
from core.models import Tag


class TagList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
  queryset = Tag.objects.all()
  serializer_class = TagSerializer

  def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
      return self.create(request, *args, **kwargs)


class TagDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
  queryset = Tag.objects.all()
  serializer_class = TagSerializer

  def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

  def put(self, request, *args, **kwargs):
      return self.update(request, *args, **kwargs)

  def delete(self, request, *args, **kwargs):
      return self.destroy(request, *args, **kwargs)
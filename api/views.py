from django.shortcuts import render
from rest_framework import mixins, generics, viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from . serializers import BookMarkSerializer, TagSerializer, CollectionSerializer
from core.models import Bookmark, Collection, Tag


class IsOwner(permissions.BasePermission):
      def has_object_permission(self, request, view, obj):
          return obj.owner == request.user


class TagViewSet(viewsets.ModelViewSet):
      queryset = Tag.objects.all()
      serializer_class = TagSerializer


class CollectionViewSet(viewsets.ModelViewSet):
      serializer_class = CollectionSerializer
      permission_classes = [IsOwner,]

      # Ensure a user only sees his/her own Collection objects.
      def get_queryset(self):
            user = self.request.user
            if user.is_authenticated:
                return Collection.objects.filter(owner=user)
            raise PermissionDenied()

      # Set user as owner of a Collection object.
      def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BookmarkViewSet(viewsets.ModelViewSet):
      serializer_class = BookMarkSerializer
      permission_classes = [IsOwner,]

      def get_queryset(self):
            user = self.request.user
            if user.is_authenticated:
                  return Bookmark.objects.filter(owner=user)
            raise PermissionDenied()

      def create(self, request, *args, **kwargs):
            data = request.data
            bookmark = Bookmark.objects.create(
                  title=data["title"],
                  url=data["url"],
                  owner=request.user
            )
            bookmark.save()

            for tag in data["tags"]:
                  tag_obj = Tag.objects.get(name=tag['name'])
                  bookmark.tags.add(tag_obj)

            for collection in data["collection"]:
                  collection_obj = Collection.objects.get(name=collection['name'])
                  bookmark.collection.add(collection_obj)

            serializer = BookMarkSerializer(bookmark)
            return Response(serializer.data)
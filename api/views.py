from django.shortcuts import render
from rest_framework import mixins, generics, viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from . serializers import TagSerializer, CollectionSerializer
from core.models import Collection, Tag


class IsOwner(permissions.BasePermission):
      def has_object_permission(self, request, view, obj):
          return obj.owner == request.user


class TagViewSet(viewsets.ModelViewSet):
      queryset = Tag.objects.all()
      serializer_class = TagSerializer


class CollectionViewSet(viewsets.ModelViewSet):
      serializer_class = CollectionSerializer
      permission_classes = [IsOwner,]

      # Ensure a user sees only own Collection objects.
      def get_queryset(self):
            user = self.request.user
            if user.is_authenticated:
                return Collection.objects.filter(owner=user)
            raise PermissionDenied()

      # Set user as owner of a Collection object.
      def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
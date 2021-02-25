from django.urls import path
from . views import TagList

urlpatterns = [
  path('tag', TagList.as_view(), name='tag-list')
]
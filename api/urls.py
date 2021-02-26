from django.urls import path
from rest_framework.routers import SimpleRouter
from . views import TagList, CollectionViewSet

router = SimpleRouter()
router.register('collections', CollectionViewSet, basename='collections')

urlpatterns = [
  path('tag', TagList.as_view(), name='tag-list')
]

urlpatterns += router.urls
from core.models import Collection
from django.urls import path
from rest_framework.routers import SimpleRouter
from . views import BookmarkViewSet, CollectionViewSet, TagViewSet

router = SimpleRouter()
router.register('collections', CollectionViewSet, basename='collections')
router.register('tags', TagViewSet, basename='tags')
router.register('bookmarks', BookmarkViewSet, basename='bookmarks')


urlpatterns = router.urls
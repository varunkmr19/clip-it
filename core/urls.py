from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('collection/create', views.create_collection_view,
         name='create_collection'),
    path('collection/edit/<int:collection_id>', views.edit_collection_view,
         name='edit_collection'),
    path('collection/<pk>/delete',
         views.CollectionDeleteView.as_view(), name='delete_collection'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('profile', views.profile_view, name='profile'),
    path('register', views.register_view, name='register'),

    path('shortcut/create', views.create_shortcut_view, name='create_shortcut'),
    path('shortcut/edit/<int:shortcut_id>',
         views.edit_shortcut_view, name='edit_shortcut'),
    path('shortcut/<pk>/delete',
         views.ShortcutDeleteView.as_view(), name='delete_shortcut'),

    path('bookmark/<int:collection_id>',
         views.load_bookmarks, name='load_bookmarks'),
    path('bookmark/create', views.create_bookmark_view, name='create_bookmark'),
    path('bookmark/edit/<int:bookmark_id>',
         views.edit_bookmark_view, name='edit_bookmark'),
    path('bookmark/<pk>/delete',
         views.BookmarkDeleteView.as_view(), name='delete_bookmark')
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('collection/create', views.create_collection_view,
         name='create_collection'),
    path('collection/edit/<int:collection_id>', views.edit_collection_view,
         name='edit_collection'),
    path('collection/delete/<int:collection_id>',
         views.delete_collection, name='delete_collection'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('profile', views.profile_view, name='profile'),
    path('register', views.register_view, name='register'),

    path('shortcut/create', views.create_shortcut_view, name='create_shortcut'),
    path('shortcut/edit/<int:shortcut_id>',
         views.edit_shortcut_view, name='edit_shortcut')
]

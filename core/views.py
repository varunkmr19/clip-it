from django import shortcuts
from django.views.generic.edit import DeleteView
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from . models import Bookmark, Collection, Shortcut, Tag


def index_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    collections = Collection.objects.filter(owner=user)
    bookmarks = Bookmark.objects.filter(owner=user)
    shortcuts = Shortcut.objects.filter(owner=user)
    return render(request, 'core/index.html', {
        'bookmarks': bookmarks,
        'collections': collections,
        'shortcuts': shortcuts
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "core/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "core/login.html")


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirm_password"]
        if password != confirmation:
            return render(request, "core/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "core/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "core/register.html")


@login_required
def profile_view(request):
    return render(request, 'core/profile.html')


@login_required
def create_collection_view(request):
    if request.method == 'POST':
        name = request.POST['collection']
        if not name:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        user = request.user
        collection = Collection.objects.create(name=name, owner=user)
        collection.save()
        return redirect('index')
    return render(request, 'core/create_collection.html')


def edit_collection_view(request, collection_id):
    try:
        collection = Collection.objects.get(
            owner=request.user, pk=collection_id)
        context = {'collection': collection}
    except Collection.DoesNotExist:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    if request.method == 'POST':
        name = request.POST['collection']
        collection.name = name
        collection.save()

        return redirect('index')
    return render(request, 'core/edit_collection.html', context)


class CollectionDeleteView(DeleteView):
    model = Collection
    success_url = "/"


@login_required
def create_shortcut_view(request):
    if request.method == 'POST':
        title = request.POST['shortcut_name']
        url = request.POST['shortcut_url']
        if not title or not url:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        user = request.user
        shortcut = Shortcut.objects.create(title=title, url=url, owner=user)
        shortcut.save()
        return redirect('index')
    return render(request, 'core/create_shortcut.html')


def edit_shortcut_view(request, shortcut_id):
    try:
        shortcut = Shortcut.objects.get(
            owner=request.user, pk=shortcut_id)
        context = {'shortcut': shortcut}
    except Shortcut.DoesNotExist:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    if request.method == 'POST':
        title = request.POST['shortcut_name']
        url = request.POST['shortcut_url']
        shortcut.title = title
        shortcut.url = url
        shortcut.save()

        return redirect('index')
    return render(request, 'core/edit_shortcut.html', context)


class ShortcutDeleteView(DeleteView):
    model = Shortcut
    success_url = "/"


def load_bookmarks(request, collection_id):
    try:
        collection = Collection.objects.get(
            pk=collection_id, owner=request.user)
        collection_name = collection.name
        shortcuts = Shortcut.objects.filter(owner=request.user)
        collections = Collection.objects.filter(owner=request.user)
        bookmarks = Bookmark.objects.filter(
            owner=request.user, collection=collection)
        context = {
            'bookmarks': bookmarks,
            'collection_name': collection_name,
            'collections': collections,
            'shortcuts': shortcuts,
            'collection_name': collection_name
        }
        return render(request, 'core/index.html', context)
    except Collection.DoesNotExist:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def create_bookmark_view(request):
    if request.method == 'POST':
        title = request.POST['title']
        url = request.POST['url']
        if not title or not url:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        collection = get_object_or_404(
            Collection, pk=request.POST.get('collection_id'))
        user = request.user
        bookmark = Bookmark.objects.create(
            title=title, url=url, owner=user)
        bookmark.save()
        bookmark.collection.add(collection)
        return redirect('index')
    collection = Collection.objects.filter(owner=request.user)
    context = {'collections': collection}
    return render(request, 'core/create_bookmark.html', context)


def edit_bookmark_view(request, bookmark_id):
    try:
        bookmark = Bookmark.objects.get(
            owner=request.user, pk=bookmark_id)
        collections = Collection.objects.filter(owner=request.user)
        context = {'bookmark': bookmark, 'collections': collections}
    except Bookmark.DoesNotExist:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    if request.method == 'POST':
        title = request.POST['title']
        url = request.POST['url']
        collection = get_object_or_404(
            Collection, pk=request.POST.get('collection_id'))
        bookmark.title = title
        bookmark.url = url
        bookmark.collection.add(collection)
        bookmark.save()

        return redirect('index')
    return render(request, 'core/edit_bookmark.html', context)


class BookmarkDeleteView(DeleteView):
    model = Bookmark
    success_url = "/"

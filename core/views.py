from django.views.generic.edit import DeleteView
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
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
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
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

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from . models import Bookmark, Collection, Tag


@login_required
def index_view(request):
    user = request.user
    collections = Collection.objects.filter(owner=user)
    bookmarks = Bookmark.objects.filter(owner=user)
    return render(request, 'core/index.html', {
        'bookmarks': bookmarks,
        'collections': collections
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


@login_required
def delete_collection(request, collection_id):
    try:
        collection = Collection.objects.get(
            owner=request.user, pk=collection_id)
    except Collection.DoesNotExist:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    if request.method == 'POST':
        collection.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

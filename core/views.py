from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render


def index_view(request):
    context = {'user': request.user}
    return render(request, 'core/index.html', context)


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

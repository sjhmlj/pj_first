from ast import Pass
from imp import get_suffixes
from django.shortcuts import render, redirect
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import get_object_or_404
from .models import User
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from reviews.models import Review


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, "Welcome!")
            return redirect("reviews:index")
        else:
            print("error")
            print(form.error_messages)
    else:
        form = CustomUserCreationForm
    context = {
        "form": form,
    }
    return render(request, "accounts/signup.html", context)


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect("reviews:index")
    else:
        form = AuthenticationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/login.html", context)


def logout(request):
    auth_logout(request)
    return redirect("reviews:index")


def detail(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    followers_number = user.followers.count()
    followings_number = user.followings.count()
    reviews_number = user.review_set.count()
    context = {
        "user": user,
        "followers_number": followers_number,
        "followings_number": followings_number,
        "reviews_number": reviews_number,
    }
    return render(request, "accounts/detail.html", context)


@login_required
def profile_update(request):

    if request.method == "POST":

        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect("accounts:detail", request.user.pk)

    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        "form": form,
    }
    print(form)
    return render(request, "accounts/update.html", context)


@login_required
def password_update(request):

    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect("accounts:detail", request.user.pk)
    else:
        form = PasswordChangeForm(request.user)
    context = {
        "form": form,
    }
    return render(request, "accounts/update.html", context)


@login_required
def delete(request):
    try:
        request.user.delete()
        auth_logout(request)
        messages.success(request, "The user is deleted")
    except:
        messages.error(request, "error")
        return render(request, "reviews:index")
    return redirect("reviews:index")


@login_required
def follow(request, pk):
    user = get_object_or_404(get_user_model, id=pk)
    if user == request.user:
        messages.warning("자신을 팔로우할 수 없습니다")
    else:
        if request.user in user.followers.all():
            user.followers.remove(request.user)
        else:
            user.followers.add(request.user)

    return redirect("account:detail", pk)

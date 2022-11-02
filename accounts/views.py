from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .models import User
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
    messages.add_message(request, messages.SUCCESS, "login")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            messages.success(request, "안녕하세요")
            return redirect("reviews:index")
    else:
        form = AuthenticationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/login.html", context)


def logout(request):
    messages.add_message(request, messages.SUCCESS, "logout")
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


from django.http import JsonResponse


@login_required
def follow(request, pk):
    user = get_object_or_404(get_user_model(), id=pk)
    if user != request.user:
        if request.user in user.followers.all():
            user.followers.remove(request.user)
            is_followed = False
        else:
            user.followers.add(request.user)
            is_followed = True
        context = {
            "is_followed": is_followed,
            "followings_count": user.followings.count(),
            "followers_count": user.followers.count(),
        }
        return JsonResponse(context)

    return redirect("accounts:detail", pk)

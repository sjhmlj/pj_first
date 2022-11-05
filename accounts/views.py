from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout, authenticate
from .models import User
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from reviews.models import Review
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from reviews.models import Review, Movie

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
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
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
        else:
            messages.warning(request, '아이디 또는 비밀번호가 틀렸습니다.')
        return redirect(request.GET.get('next') or 'reviews:index')
    else:
        form = AuthenticationForm()
        context = {
            'form':form,
            }
        return render(request, 'accounts/login.html', context)

def logout(request):
    auth_logout(request)
    return redirect("reviews:index")

@login_required
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
@require_POST
def delete(request):
    try:
        request.user.delete()
        auth_logout(request)
        messages.success(request, "탈퇴하였습니다.")
    except:
        messages.error(request, "error")
        return render(request, "reviews:index")
    return redirect("reviews:index")

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

@login_required
def reviews(request, pk):
    user = get_object_or_404(get_user_model(), id=pk)
    reviews = Review.objects.filter(user=user)
    context = {
        "reviews": reviews,
        "user": user,
    }
    return render(request, "accounts/reviews.html", context)

@login_required
def showfollow(request, pk):
    user = get_object_or_404(get_user_model(), id=pk)
    followers = user.followers.all()
    followings = user.followings.all()
    context = {
        "followers": followers,
        "followings": followings,
    }
    return render(request, "accounts/show_follow.html", context)

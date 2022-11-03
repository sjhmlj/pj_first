from django.shortcuts import get_object_or_404, render, redirect
from .forms import MovieForm, ReviewForm, CommentForm
from .models import Movie, Review, Comment
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Avg

def index(request):
    context = {
        'movies': Movie.objects.all(),
    }
    return render(request, 'reviews/index.html', context)

@login_required
def movie_create(request):
    if request.user.is_superuser:
        if request.method == "POST":
            movie_form = MovieForm(request.POST, request.FILES)
            if movie_form.is_valid():
                form = movie_form.save(commit=False)
                form.opening_date = request.POST.get('opening_date')
                form.save()
                return redirect('reviews:index')
        else:
            movie_form = MovieForm()
        context = {
            'form':movie_form,
        }
        return render(request, 'reviews/movie_create.html', context)
    else:
        messages.warning(request, '관리자 권한입니다.')
        return redirect('reviews:index')

def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    context = {
        'movie': movie,
        'reviews': movie.review_set.all(),
        'total' : movie.review_set.aggregate(review_avg=Avg('grade')),
    }
    return render(request, 'reviews/movie_detail.html', context)

@login_required
def movie_update(request, movie_pk):
    if request.user.is_superuser:
        movie = get_object_or_404(Movie, pk=movie_pk)
        if request.method == "POST":
            form = MovieForm(request.POST, request.FILES, instance=movie)
            if form.is_valid():
                form.save()
                return redirect('reviews:movie_detail', movie_pk)
        else:
            form = MovieForm(instance=movie)
        context = {
            'form':form,
        }
        return render(request, 'reviews/movie_update.html', context)
    else:
        messages.warning(request, '관리자 권한입니다.')
        return redirect('reviews:index')

@login_required
def review_create(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            form = review_form.save(commit=False)
            form.movie = movie
            form.user = request.user
            form.grade = request.POST.get('grade')
            form.save()
            messages.success(request, '리뷰가 등록되었습니다.')
            return redirect('reviews:movie_detail', movie_pk)
    else:
        review_form = ReviewForm()
    context = {
        'review_form' : review_form,
    }
    return render(request, 'reviews/review_create.html', context)

@login_required
def review_detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    context = {
        'review': review,
        'comment_form': CommentForm(),
        'comments': review.comment_set.all(),
    }
    return render(request, 'reviews/review_detail.html', context)

@login_required
def review_update(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'POST' and review.user == request.user:
        review_form = ReviewForm(request.POST, instance=review)
        if review_form.is_valid():
            form = review_form.save(commit=False)
            form.grade = request.POST.get('grade')
            form.save()
            messages.success(request, '수정되었습니다.')
            return redirect('reviews:review_detail', review.pk)
    else:
        review_form = ReviewForm(instance=review)
    context = {
        'review_form' : review_form,
    }
    return render(request, 'reviews/review_update.html', context)
    
@login_required
def review_delete(request, movie_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == "POST" and review.user == request.user:
        review.delete()
        messages.success(request, '성공적으로 탈퇴되었습니다.')
    else:
        messages.warning(request, '잘못된 접근입니다.')
    return redirect('reviews:movie_detail', movie_pk)

@login_required
def comment_create(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            form = comment_form.save(commit=False)
            form.user = request.user
            form.review = review
            form.save()
            return redirect('reviews:review_detail', review_pk)

@login_required
def comment_delete(request, review_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == "POST" and comment.user == request.user:
        comment.delete()
    return redirect('reviews:review_detail', review_pk)

@login_required
def like(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if review.like_users.filter(pk=request.user.pk).exists():
        review.like_users.remove(request.user)
        isLiked = False
    else:
        review.like_users.add(request.user)
        isLiked = True
    context = {
        'isLiked':isLiked,
        'likeCount':review.like_users.count(),
    }
    return JsonResponse(context)

def comment_like(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if comment.like_users.filter(pk=request.user.pk).exists():
        comment.like_users.remove(request.user)
    else:
        comment.like_users.add(request.user)
    return redirect('reviews:review_detail', comment.review.pk)

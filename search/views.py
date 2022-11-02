from django.shortcuts import render
from accounts.models import User
from reviews.models import Review, Movie
from django.db.models import Q

# Create your views here.


def searchResult(request):
    user = None
    review = None
    movie = None
    query = None
    if "q" in request.GET:
        query = request.GET.get("q")
        user = User.objects.all().filter(Q(username__contains=query))
        review = Review.objects.all().filter(
            Q(title__contains=query) | Q(content__contains=query)
        )
        movie = Review.objects.all().filter(
            Q(title__contains=query) | Q(content__contains=query)
        )
    context = {
        "query": query,
        "user": user,
        "review": review,
        "movie": movie,
    }
    return render(request, "search/search.html", context)

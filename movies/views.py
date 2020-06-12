from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .models import Movie, Review, Genre
from django.contrib.auth import get_user_model
from django.http import JsonResponse

from .forms import ReviewForm

# Create your views here.
def welcome(request):
    return render(request, 'movies/welcome.html')

def recommand():
    # 추천알고리즘 적용할 함수
    pass

def find_genre():
    pass

def index(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies,
    }
    return render(request, 'movies/index.html', context)

def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    # same_genres = Movie.objects.filter()
    reviews = Review.objects.all(movie_id=movie.pk)
    context = {
        'movie': movie,
        # 'same_genres': same_genres,
        'reviews': reviews,
    }
    # 같은 장르의 평점 높은 영화
    # 베스트 리뷰, 일반 리뷰
    return render(request, 'movies/movie_detail.html', context)

def review_create(request, movie_pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=movie_pk)
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.movie = movie
                review.save()
            return redirect('movies:review_detail', review.pk)
        else:
            form = ReviewForm()
        context = {'form':form, 'movie':movie}
        return render(request, 'movies/review_create.html', context)
    else:
        return redirect('accounts:login')


def review_detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    context = {
        'review': review,
    }
    return render(request, 'movies/review_detail.html', context)

@require_POST
def review_delete(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    movie_pk = review.movie_id
    if request.user == review.user:
        review.delete()
    return redirect('movies:movie_detail', movie_pk)

def review_update(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.user == review.user:
        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                review = form.save()
                return redirect('movies:review_detail', review.pk)
        else:
            form = ReviewForm(instance=review)
        context = {'form': form}
        return render(request, 'movies/review_create.html', context)
    else:
        return redirect('movies:review_detail', review.pk)

def like(request, review_pk):
    user = request.user
    review = get_object_or_404(Review, pk=review_pk)

    if review.like_users.filter(id=user.pk).exists():
        review.like_users.remove(user)
    else:
        review.like_users.add(user)
    
    return redirect('movies:review_detail', review_pk)

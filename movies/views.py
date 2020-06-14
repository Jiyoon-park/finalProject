from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .models import Movie, Review, Genre
from django.contrib.auth import get_user_model
from django.http import JsonResponse

import numpy as np
import pandas as pd

from .forms import ReviewForm

# Create your views here.
def welcome(request):
    return render(request, 'movies/welcome.html')

def pearsonR(s1, s2):
    s1_c = s1 - s1.mean()
    s2_c = s2 - s2.mean()
    return np.sum(s1_c * s2_c) / np.sqrt(np.sum(s1_c ** 2) * np.sum(s2_c ** 2))

def recommend(Id):
    # 추천알고리즘 적용할 함수
    review = pd.DataFrame(data=Review.objects.all().values('user_id', 'movie_id', 'score'))
    review = review.rename(columns={"user_id":"userId", "movie_id":"movieId"})
    movie = pd.DataFrame(data=Movie.objects.all().values('id', 'original_title', 'original_language'))
    movie = movie.rename(columns={"id":"movieId"})

    movie.movieId = pd.to_numeric(movie.movieId, errors='coerce')
    review.movieId = pd.to_numeric(review.movieId, errors='coerce')

    data = pd.merge(review, movie, on='movieId', how='inner')

    matrix = data.pivot_table(index='movieId', columns='userId', values='score')

    result = []
    
    for side_id in matrix.columns:
        
        if side_id == Id:
            continue

        cor = pearsonR(matrix[Id], matrix[side_id])

        if np.isnan(cor) or cor < 0:
            continue
        else:
            result.append((side_id, cor))
            
    result.sort(key=lambda r: -r[1])
    result = max(result, key=lambda r: -r[1])[0]

    movies = Review.objects.filter(user_id=Id).values('movie_id')
    movies = [value['movie_id'] for value in movies]

    sim_movie = Review.objects.filter(user_id=result).values('movie_id')
    
    return [value['movie_id'] for value in sim_movie if value['movie_id'] not in movies]

def index(request):
    movies = Movie.objects.all()[:5]
    if request.user.is_authenticated:
        r_movies = Movie.objects.filter(id__in=recommend(request.user.id)).order_by('-popularity')[:5]
    else: r_movies = []
    context = {
        'movies': movies,
        'r_movies': r_movies
    }
    return render(request, 'movies/index.html', context)

def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    reviews = Review.objects.filter(movie_id=movie.pk)
    # 같은 장르의 평점 높은 영화
    same_genres = Movie.objects.filter(genres__in=movie.genres.all()).distinct().order_by('-popularity')[:3]
    
    genres = Genre.objects.all()

    g_movies = {
        t.name: Movie.objects.filter(genres__in=t.id)
        for t in genres
    }
    
    context = {
        'movie': movie,
        'same_genres': same_genres,
        'reviews': reviews,
        'g_movies': g_movies,
    }
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
from django.urls import path
from . import views

app_name="movies"
urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('index/', views.index, name='index'),
    path('<int:movie_pk>/detail/', views.movie_detail, name='movie_detail'),
    path('<int:movie_pk>/review_create/', views.review_create, name='review_create'),
    path('<int:review_pk>/review_detail/', views.review_detail, name='review_detail'),
    path('<int:review_pk>/review_update/', views.review_update, name='review_update'),
    path('<int:review_pk>/review_delete/', views.review_delete, name='review_delete'),
    path('<int:review_pk>/like/', views.like, name='like'),
]
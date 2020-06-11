from django.urls import path
from . import views

app_name="movies"
urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('index/', views.index, name='index'),
]
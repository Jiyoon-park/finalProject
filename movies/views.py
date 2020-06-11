from django.shortcuts import render

# Create your views here.
def welcome(request):
    return render(request, 'movies/welcome.html')

def index(request):
    return render(request, 'movies/index.html')
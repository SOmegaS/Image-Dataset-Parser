from django.shortcuts import render
from .forms import *


def index(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            info = form.cleaned_data
            print(info.get('list_of_names'))
            print(info.get('count_image'))
    else:
        form = PostForm()
    return render(request, 'main/index.html', {'form': form})


def about(request):
    return render(request, 'main/about.html')

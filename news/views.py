from django.shortcuts import render

# Create your views here.


def home(request):
    context = {
        'articles': [1,2,3]
    }
    return render(request, 'news/home.html', context)

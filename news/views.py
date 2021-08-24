from django.shortcuts import render
from newsapi import NewsApiClient
from decouple import config
# Create your views here.

news_api = NewsApiClient(api_key=config('NEWSAPI_KEY'))


def home(request):

    head_lines = news_api.get_top_headlines(sources='ign, cnn', page_size=100)
    articles = head_lines['articles']

    return render(request, 'news/home.html', {'articles': articles})

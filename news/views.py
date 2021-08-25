from django.shortcuts import render
from newsapi import NewsApiClient
from decouple import config
from .models import Country,Source

news_api = NewsApiClient(api_key=config('NEWSAPI_KEY'))


def home(request):

    head_lines = news_api.get_top_headlines(sources='ign, cnn')
    articles = head_lines['articles']
    countries = Country.objects.all()
    sources = Source.objects.all()

    return render(request, 'news/home.html', {'articles': articles, 'countries': countries, 'sources': sources})

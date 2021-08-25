from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from newsapi import NewsApiClient
from decouple import config
from .models import Country, Source

news_api = NewsApiClient(api_key=config('NEWSAPI_KEY'))


def home(request):
    if request.method == "POST":
        country = request.POST.get('country', '')
        source = request.POST.get('source', '')
        if country:
            head_lines = news_api.get_top_headlines(language=None, country=country)
        elif source:
            head_lines = news_api.get_top_headlines(language=None, sources=source)
    else:
        head_lines = news_api.get_top_headlines()

    articles = head_lines['articles']
    countries = Country.objects.all()
    sources = Source.objects.all()

    return render(request, 'news/home.html', {'articles': articles, 'countries': countries, 'sources': sources})

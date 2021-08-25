from django.shortcuts import render
from newsapi import NewsApiClient
from decouple import config
from .models import Country, Source

news_api = NewsApiClient(api_key=config('NEWSAPI_KEY'))


def home(request):
    countries = Country.objects.all()
    sources = Source.objects.all()
    selected_country = 'all'
    selected_source = 'all'

    if request.method == "POST":
        country = request.POST.get('country', '')
        source = request.POST.get('source', '')
        if country:
            head_lines = news_api.get_top_headlines(language=None, country=country)
            selected_country = countries.get(code=country).name
        elif source:
            head_lines = news_api.get_top_headlines(language=None, sources=source)
            selected_source = sources.get(code=source).name
    else:
        head_lines = news_api.get_top_headlines()

    articles = head_lines['articles']

    return render(request, 'news/home.html', {
            'articles': articles,
            'countries': countries,
            'sources': sources,
            'selected_country': selected_country,
            'selected_source': selected_source,
    })

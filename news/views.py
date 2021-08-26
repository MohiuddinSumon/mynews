from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
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

    # articles = {}

    return render(request, 'news/home.html', {
            'articles': articles,
            'countries': countries,
            'sources': sources,
            'selected_country': selected_country,
            'selected_source': selected_source,
    })


@login_required
def custom_picks(request):
    user = request.user
    print(f"USER = {user}, Profile = {request.user.profile}, ")

    countries_qs = user.profile.country.all()
    sources_qs = user.profile.source.all()
    keyword = user.profile.keyword
    if keyword:
        keyword = keyword[0].split()

    result = []

    for country in countries_qs:
        head_lines = news_api.get_top_headlines(language=None, country=country.code, page_size=2)
        result.append(head_lines.get('articles'))

    print((result))

    source = ''
    for src in sources_qs:
        source += src.code + ', '
        print(src.code, source)
    print(source)
    print('\n')

    head_lines = news_api.get_top_headlines(language=None, sources=source)
    result.append(head_lines.get('articles'))
    print(len(result))

    # articles = {}

    return render(request, 'news/home.html', {
            'articles': result,
            'countries': "countries",
            'sources': "sources",
            'selected_country': "selected_country",
            'selected_source': "selected_source",
    })

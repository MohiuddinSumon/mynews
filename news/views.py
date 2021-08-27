from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Country, Source, News
from . import news_api


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

    countries_qs = user.profile.country.all()
    sources_qs = user.profile.source.all()
    keyword = user.profile.keyword
    if keyword:
        keyword = keyword[0].split()

    results = []

    for country in countries_qs:
        head_lines = news_api.get_top_headlines(language=None, country=country.code)
        results.extend(head_lines.get('articles'))

    source = ''
    for src in sources_qs:
        source += src.code + ', '
    if source:
        head_lines = news_api.get_top_headlines(language=None, sources=source)
        results.extend(head_lines.get('articles'))

    for result in results:
        News.objects.get_or_create(user=user,
                                   source=result.get('source').get('name', 'default'),
                                   title=result.get('title'),
                                   description=result.get('description'),
                                   url=result.get('url'),
                                   publish_date=result.get('publishedAt'),
                                   image_url=result.get('urlToImage', 'no image provided'))

    return render(request, 'news/picks.html', {
            'articles': results,
    })

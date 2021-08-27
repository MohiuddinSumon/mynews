from celery import Celery
from celery.schedules import crontab
from django.contrib.auth.models import User
from . import news_api
from mynews.celery import app
from news.models import News


@app.task
def fetch_news_for_user():
    users = User.objects.all()
    for user in users:
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


app.conf.timezone = "Asia/Dhaka"
app.conf.beat_schedule = {
    'fetch-user-news': {
        'task': 'mynews.news.tasks.fetch_news_for_user',
        'schedule': crontab(minute='*/15')
    }
}

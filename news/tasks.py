from celery.schedules import crontab
from decouple import config
from django.contrib.auth.models import User
from django.core.mail import send_mail

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
        keywords = []
        if keyword:
            keywords = keyword[0].split()

        results = []

        for country in countries_qs:
            head_lines = news_api.get_top_headlines(language=None, country=country.code)
            results.extend(head_lines.get('articles'))

        for word in keywords:
            head_lines = news_api.get_top_headlines(language=None, q=word)
            results.extend(head_lines.get('articles'))

        source = ''
        for src in sources_qs:
            source += src.code + ', '
        if source:
            head_lines = news_api.get_top_headlines(language=None, sources=source)
            results.extend(head_lines.get('articles'))

        for result in results:
            try:
                News.objects.get_or_create(user=user,
                                           source=result.get('source').get('name', 'default'),
                                           title=result.get('title'),
                                           description=result.get('description'),
                                           url=result.get('url'),
                                           publish_date=result.get('publishedAt'),
                                           image_url=result.get('urlToImage', 'no image provided'))
            except Exception:
                pass


@app.task
def send_email_for_keyword_news():
    users = User.objects.all()
    for user in users:
        keyword = user.profile.keyword
        keywords = []
        if keyword:
            keywords = keyword[0].split()

        news_found = False
        for word in keywords:
            head_lines = news_api.get_top_headlines(language=None, q=word)
            if head_lines.get('totalResults', 0) > 0:
                news_found = True
                break

        if news_found:
            from_email = config('FROM_EMAIL')
            send_mail(subject='You Have News!!',
                      message='Hey you have new news to check on the site. ',
                      from_email=None,
                      recipient_list=[user.email],
                      fail_silently=False)


app.conf.timezone = "Asia/Dhaka"
app.conf.beat_schedule = {
    'fetch-user-news': {
        'task': 'news.tasks.fetch_news_for_user',
        'schedule': crontab(minute='*/15')
    },
    'send-email-for-keyword': {
        'task': 'news.tasks.send_email_for_keyword_news',
        'schedule': crontab(minute=0, hour='*/3,8-18')  # every 3 hour between 8AM to 6 PM
    },
}

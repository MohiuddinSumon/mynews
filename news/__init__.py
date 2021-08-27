from decouple import config
from newsapi import NewsApiClient


news_api = NewsApiClient(api_key=config('NEWSAPI_KEY'))

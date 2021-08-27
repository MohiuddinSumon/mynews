from django.urls import path
from .views import home, UserNewsListView, UserNewsAPI

urlpatterns = [
    path('', home, name='home'),
    path('picks/', UserNewsListView.as_view(), name='picks'),
    path('news-api/', UserNewsAPI.as_view(), name='news-api'),
]

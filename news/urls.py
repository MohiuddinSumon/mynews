from django.urls import path
from .views import home, UserNewsListView

urlpatterns = [
    path('', home, name='home'),
    path('picks/', UserNewsListView.as_view(), name='picks'),
]

from django.urls import path
from .views import home, custom_picks

urlpatterns = [
    path('', home, name='home'),
    path('picks/', custom_picks, name='picks'),
]

from django.contrib.auth.models import User
from django.db import models


class Country(models.Model):
    code = models.CharField(max_length=2, unique=True, blank=False)
    name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class Source(models.Model):
    code = models.CharField(max_length=50, unique=True, blank=False)
    name = models.CharField(max_length=250, unique=True, blank=False)
    description = models.TextField(null=True, blank=True)
    url = models.URLField()
    category = models.CharField(max_length=50, null=True, blank=True)
    language = models.CharField(max_length=2, null=True, blank=False)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, related_name='sources')

    def __str__(self):
        return self.name


class News(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news')
    source = models.TextField(null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    url = models.TextField(unique=True)
    image_url = models.TextField(null=True, blank=True)
    publish_date = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} pk= {self.pk}'

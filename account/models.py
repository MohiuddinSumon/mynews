from django.db import models
from django.contrib.auth.models import User
from news.models import Country, Source
from django.contrib.postgres.fields import ArrayField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.ManyToManyField(Country, related_name='profiles')
    source = models.ManyToManyField(Source, related_name='profiles')
    keyword = ArrayField(models.CharField(max_length=255), blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile, id = {self.pk}'


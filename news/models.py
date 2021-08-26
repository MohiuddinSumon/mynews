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

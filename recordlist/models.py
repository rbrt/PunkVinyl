from django.db import models


class Records(models.Model):
    image = models.TextField(db_column=u'Image')
    band = models.TextField(db_column=u'Band')
    link = models.TextField(db_column=u'Link')
    album = models.TextField(db_column=u'Album')
    price = models.FloatField(db_column=u'Price')
    vinyl = models.IntegerField(db_column=u'Vinyl')
    sitename = models.TextField(db_column=u'Sitename')
    date = models.TextField(db_column='Date')
    id = models.IntegerField(blank=True, primary_key=True)

    class Meta:
        db_table = u'Records'


class Blog(models.Model):
    title = models.TextField(db_column=u'Title')
    text = models.TextField(db_column=u'Text')
    date = models.TextField(db_column=u'Date')
    id = models.IntegerField(blank=True, primary_key=True)

    class Meta:
        db_table = u'Blogs'
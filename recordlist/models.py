from django.db import models


class Records(models.Model):
    image = models.TextField(db_column=u'Image', blank=True)
    band = models.TextField(db_column=u'Band', blank=True)
    link = models.TextField(db_column=u'Link', blank=True)
    album = models.TextField(db_column=u'Album', blank=True)
    price = models.FloatField(null=True, db_column=u'Price', blank=True)
    vinyl = models.IntegerField(null=True, db_column=u'Vinyl', blank=True)
    sitename = models.TextField(db_column=u'Sitename', blank=True)
    date = models.TextField(db_column='Date', blank=True)
    id = models.IntegerField(blank=True, primary_key=True)


    class Meta:
        db_table = u'Records'
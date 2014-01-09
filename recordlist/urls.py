from django.conf.urls import patterns, url

import views

urlpatterns = patterns(
    '',
    url(r'^$', views.RecordListAll.as_view(), name="list_all"),
    url(r'^distros$', views.RecordListDistro.as_view(), name="distros"),
    url(r'^search$', views.RecordListSearch.as_view(), name="search"),
    url(r'^latest$', views.RecentlyAddedRecords.as_view(), name="latest"),
)
from django.conf.urls import patterns, url

import views

urlpatterns = patterns(
    '',
    url(r'^$', views.RecordListAll.as_view(), name="list_all"),
    url(r'^distros$', views.RecordListDistro.as_view(), name="distros"),
)
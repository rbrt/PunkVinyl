from django.conf.urls import patterns, url

import views

urlpatterns = patterns(
    '',
    url('', views.RecordList.as_view())
)
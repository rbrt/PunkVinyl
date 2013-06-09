from django.conf.urls import patterns, include, url
from django.contrib import admin

import recordlist.urls
import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', views.MainPageView.as_view(), name="index"),
    url(r'^contact/', views.ContactPageView.as_view(), name="contact"),
    url(r'^recordlist/', include(recordlist.urls, namespace="recordlist")),
    url(r'^admin/', include(admin.site.urls)),
)

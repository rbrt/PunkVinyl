from django.conf.urls import patterns, include, url
from django.contrib import admin

import recordlist.urls

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^recordlist/', include(recordlist.urls)),
    url(r'^admin/', include(admin.site.urls)),
)

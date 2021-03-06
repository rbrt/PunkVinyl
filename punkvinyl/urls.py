from django.conf.urls import patterns, include, url
from django.contrib import admin

import recordlist.urls
import blog.urls
import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', views.MainPageView.as_view(), name="index"),
    url(r'^login/', views.LoginView.as_view(), name="login"),
    url(r'^contact/', views.ContactPageView.as_view(), name="contact"),
    url(r'^blog/', include(blog.urls, namespace="blog")),
    url(r'^recordlist/', include(recordlist.urls, namespace="recordlist")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ben/$', recordlist.views.BenPage.as_view(), name="ben"),
    url(r'^bensuccess/$', recordlist.views.BenSuccessPage.as_view(), name="bensuccess"),
    url(r'^benfail/$', recordlist.views.BenFailPage.as_view(), name="benfail")
)

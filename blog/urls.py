from django.conf.urls import patterns, url

import views

urlpatterns = patterns(
    '',
    url(r'^$', views.BlogView.as_view(), name="blog"),
    url(r'^add_blog$', views.BlogUpdatePage.as_view(), name="add_blog"),
    url(r'^add_blog_success$', views.BlogUpdateFailPage.as_view(), name="add_blog_success"),
    url(r'^add_blog_failure$', views.BlogUpdateSuccessPage.as_view(), name="add_blog_failure"),
)

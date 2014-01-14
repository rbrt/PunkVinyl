from datetime import datetime as dt
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from punkvinyl import forms

from recordlist.models import Blog
from scraper import database


class BlogView(TemplateView):
    template_name = "blog.html"

    def parseDate(self, record):
        recDate = record.date.split('-')
        date = dt(year=int(recDate[0]),
                  month=int(recDate[1]),
                  day=int(recDate[2]),
                  hour=int(recDate[3]),
                  minute=int(recDate[4]),
                  second=int(recDate[5]))
        return date

    def getLatest(self, blogs):
        minDate = dt.min
        sortedList = sorted(blogs, key=(lambda x: (self.parseDate(x) - minDate).seconds), reverse=True)[:60]
        return sortedList

    def get_context_data(self, *args, **kwargs):
        response = super(BlogView, self).get_context_data(*args,**kwargs)

        blogs = self.getLatest(Blog.objects.all())

        response.update({
            'blogs':blogs
        })
        return response


class BlogUpdatePage(TemplateView):
    template_name = "add_blog.html"

    def getId(self):
        blog = Blog.objects.all()
        if len(blog) == 0:
            return 1
        return blog[len(blog) - 1].id + 1

    def post(self, request):
        title = request.POST['title']
        text = request.POST['text']
        date = database.currentDate()
        id = self.getId()

        if '' not in [title, text, date, id]:
            Blog.objects.create(title=title,
                                text=text,
                                date=date,
                                id=id)
            return HttpResponseRedirect(reverse('blog:add_blog_success'))
        else:
            return HttpResponseRedirect(reverse('blog:add_blog_fail'))

    def get_context_data(self, *args, **kwargs):
        response = super(BlogUpdatePage, self).get_context_data(*args, **kwargs)

        if self.request.user.is_authenticated():
            form = forms.BlogForm()
            response.update({
                'form': form,
            })
            return response
        else:
            form = forms.LoginForm()
            response.update({
                'need_login': True,
                'form': form,
                'next': reverse("blog:add_blog")
            })
            return response


class BlogUpdateFailPage(BlogUpdatePage):
    template_name = "add_blog_failure.html"


class BlogUpdateSuccessPage(BlogUpdatePage):
    template_name = "add_blog_success.html"

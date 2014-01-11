from datetime import datetime as dt

from django.views.generic import TemplateView

from recordlist.models import Blog


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

    def getLatest(self, records):
        minDate = dt.min
        sortedList = sorted(records, key=(lambda x: (self.parseDate(x) - minDate).seconds), reverse=True)[:60]
        return sortedList

    def get_context_data(self, *args, **kwargs):
        response = super(BlogView, self).get_context_data(*args,**kwargs)

        blogs = self.getLatest(self, Blog.objects.all())

        response.update({
            'blogs':blogs
        })
        return response

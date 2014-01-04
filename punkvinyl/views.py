from django.shortcuts import render_to_response, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic.base import TemplateView, ContextMixin, TemplateResponseMixin
from recordlist.models import Records

import recordlist.urls


class SearchMixin(TemplateResponseMixin):
    def get_context_data(self, **kwargs):
        if 'searchvalue' in self.request.GET:

            return redirect('127.0.0.1:8000/recordlist/')

            #return render_to_response('recordlist.html', response_context)
        else:
            super(SearchMixin, self).get_context_data(**kwargs)


class MainPageView(TemplateView):
    template_name = "main.html"


class ContactPageView(TemplateView):
    template_name = "contact.html"

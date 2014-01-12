from datetime import datetime as dt
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic.base import TemplateView
from punkvinyl import forms

from recordlist.models import Records
from scraper import database


class DisplayRecords(TemplateView):

    def get_record_list(self):
        return Records.objects.all().order_by('band')

    def get_context_data(self, *args, **kwargs):
        record_list = self.get_record_list()
        response = super(DisplayRecords, self).get_context_data(*args,**kwargs)

        sorted(record_list)
        record_list_a = []
        record_list_b = []

        alt = True
        for record in record_list:
            if alt:
                record_list_a.append(record)
            else:
                record_list_b.append(record)
            alt = not alt

        if len(record_list) % 2 is not 0:
            record_list = zip(record_list_a, record_list_b)
            record_list.append((record_list_a[-1], None))
        else:
            record_list = zip(record_list_a, record_list_b)

        # Break all the records into groups of group_size
        record_group = []
        group_size = 20
        for i in range(0, (len(record_list) / group_size) + 1):
            record_group.append(record_list[0+i*group_size:group_size+i*group_size:])
        try:
            index = int(self.request.GET['page'])
        except MultiValueDictKeyError:
            index = 1
        except ValueError:
            command = self.request.GET['page']
            if 'prev' in command:
                change = int(command[4:])
                index = (change-1) % len(record_group)
            elif 'next' in command:
                change = int(command[4:])
                index = (change+1) % len(record_group)

        list_size = len(record_group)
        record_group = record_group[index-1]

        print list_size

        response.update({
            'record_group': record_group,
            'record_count': range(1, list_size+1),
            'index':index
        })
        return response


class RecordListAll(DisplayRecords):
    template_name = "recordlist.html"


class RecordListSearch(DisplayRecords):
    template_name = "search.html"

    def filter_results(self, records=None, band=None, album=None, distro=None):
        newlist = []
        for record in records:
            if (band.lower() in record.sitename.lower() or
                band.lower() in record.band.lower() or
                band.lower() in record.album.lower()):
                newlist.append(record)

        return newlist

    def get_record_list(self):
        search_term = self.request.GET['searchvalue']
        return self.filter_results(records=Records.objects.all(), band=search_term)

    def get_context_data(self, *args, **kwargs):
        response = super(RecordListSearch, self).get_context_data(*args, **kwargs)
        search_term = self.request.GET['searchvalue']
        response.update({
            'search_term':"searchvalue="+search_term,
            'search_term_short':search_term
        })
        return response


class RecentlyAddedRecords(DisplayRecords):
    template_name = "latest.html"

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

    def get_record_list(self):
        return self.getLatest(Records.objects.all())


class RecordListDistro(TemplateView):
    template_name = "distrolist.html"


class BenPage(TemplateView):
    template_name = "ben.html"

    def post(self, request):
        image = request.POST['image']
        band = request.POST['band']
        link = request.POST['link']
        album = request.POST['album']
        price = request.POST['price']
        vinyl = request.POST['vinyl']
        sitename = "Crasher Dust"
        date = database.currentDate()
        id = database.getId()

        if None not in [image, band, link, album, price, vinyl, sitename, date, id]:
            Records.objects.create(image=image,
                                   band=band,
                                   link=link,
                                   album=album,
                                   price=price,
                                   vinyl=vinyl,
                                   sitename=sitename,
                                   date=date,
                                   id=id)
            return HttpResponseRedirect(reverse('bensuccess'))
        else:
            return HttpResponseRedirect(reverse('benfail'))


    def get_context_data(self, *args, **kwargs):
        response = super(BenPage, self).get_context_data(*args,**kwargs)

        if self.request.user.is_authenticated():
            form = forms.BenForm()
            response.update({
                'form': form,
            })
            return response
        else:
            form = forms.LoginForm()
            response.update({
                'need_login': True,
                'form': form,
                'next': reverse("recordlist:ben")
            })
            return response


class BenSuccessPage(BenPage):
    template_name = "bensuccess.html"


class BenFailPage(BenPage):
    template_name = "benfail.html"
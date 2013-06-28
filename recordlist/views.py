from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic.base import TemplateView

from recordlist.models import Records


class RecordListAll(TemplateView):
    template_name = "recordlist.html"

    def get_context_data(self, *args, **kwargs):
        response = super(RecordListAll, self).get_context_data(*args,**kwargs)
        record_list = Records.objects.all().order_by('band')

        sorted(record_list)
        print record_list[len(record_list)-1].album
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
        group_size = 40
        for i in range(0, (len(record_list) / group_size) + 1):
            record_group.append(record_list[0+i*group_size:20+i*group_size:])
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


class RecordListDistro(TemplateView):
    template_name = "distrolist.html"

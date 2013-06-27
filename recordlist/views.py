import json

from django.views.generic.base import TemplateView

from recordlist.models import Records


class RecordListAll(TemplateView):
    template_name = "recordlist.html"

    def get_context_data(self, *args, **kwargs):
        response = super(RecordListAll, self).get_context_data(*args,**kwargs)
        record_list = Records.objects.all().order_by('band')

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

        record_list = zip(record_list_a, record_list_b)

        # Break all the records into groups of 20
        record_group = []
        for i in range(0, len(record_list) / 20):
            record_group.append(record_list[0+i*20:10+i*20:])

        #[ [ (,) ] ]
        # list of list of pairs

        records_as_json = json.dumps(["test",{"record":record_group[0][0][0].image}], separators=(',',':'))
        print records_as_json


        response.update({
            'record_group': record_group,
            'record_count': range(0, len(record_group)),
            'list_size': len(record_group)
        })
        return response


class RecordListDistro(TemplateView):
    template_name = "distrolist.html"

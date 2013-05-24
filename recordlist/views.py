from django.views.generic.base import TemplateView
from recordlist.models import Records

class RecordList(TemplateView):
    template_name = "recordlist.html"

    def get_context_data(self, *args, **kwargs):
        response = super(RecordList, self).get_context_data(*args,**kwargs)
        record_list = Records.objects.all().order_by('band')

        record_list_a = []
        record_list_b = []

        alt = True
        for record in record_list:
            if alt:
                record_list_a.append(record)
            else:
                record_list_b.append(record)
            alt = not alt
            print record

        print record_list
        print "FUUUUUUUUUUUUUUUUCK"
        print record_list_a


        response.update({
            'record_list_a': record_list_a,
            'record_list_b': record_list_b
        })
        return response

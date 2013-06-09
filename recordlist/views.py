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

        response.update({
            'record_list': record_list
        })
        return response


class RecordListDistro(TemplateView):
    template_name = "distrolist.html"

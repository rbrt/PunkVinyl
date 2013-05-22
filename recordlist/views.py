from django.views.generic.base import TemplateView
from recordlist.models import Records

class RecordList(TemplateView):
    template_name = "recordlist.html"

    def get_context_data(self, *args, **kwargs):
        response = super(RecordList, self).get_context_data(*args,**kwargs)
        record_list = Records.objects.all().order_by('band')
        response.update({
            'record_list': record_list
        })
        return response

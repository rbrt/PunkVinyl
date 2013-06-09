from django.views.generic.base import TemplateView

class MainPageView(TemplateView):
    template_name = "main.html"

class ContactPageView(TemplateView):
    template_name = "contact.html"

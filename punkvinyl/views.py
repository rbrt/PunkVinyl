from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView

from punkvinyl.forms import LoginForm


class MainPageView(TemplateView):
    template_name = "main.html"


class ContactPageView(TemplateView):
    template_name = "contact.html"


class LoginView(TemplateView):
    template_name = "login.html"

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('../')
        else:
            return HttpResponseRedirect('')


    def get_context_data(self, **kwargs):
        response = super(LoginView, self).get_context_data(**kwargs)

        if self.request.method == "GET":
            form = LoginForm()
            response.update({
                'form': form
            })

        return response


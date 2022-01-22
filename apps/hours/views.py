from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.views import generic

from hours.models import *


class EnterHours(LoginRequiredMixin, generic.TemplateView):
    login_url = 'entry:login'
    template_name = 'hours/entry.html'


class ViewHours(LoginRequiredMixin, generic.ListView):
    login_url = 'entry:login'
    template_name = 'hours/view.html'
    model = Log

    def get_queryset(self):
        if self.request.user is Mentor:
            return Log.objects.all()
        elif self.request.user is Gremlin:
            return Log.objects.get(gremlin__user=self.request.user)



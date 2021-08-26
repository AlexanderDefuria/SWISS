from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic


class Index(generic.TemplateView):
    template_name = 'promotional/Index.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('entry:index'))
        else:
            return super(Index, self).get(request, *args, **kwargs)

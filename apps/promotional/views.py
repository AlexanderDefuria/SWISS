from django.shortcuts import render

# Create your views here.
from django.views import generic


class Index(generic.TemplateView):
    template_name = 'promotional/Index.html'

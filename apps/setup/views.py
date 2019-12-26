from django.shortcuts import render
from django.views import generic


# Create your views here.

class Import_TBA(generic.TemplateView):
    template_name = "setup/Import_TBA.html"



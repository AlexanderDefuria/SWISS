from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('promotional:index'), permanent=True)),
    path('enter', views.ViewHours.as_view(), name='enter'),
    path('view', views.EnterHours.as_view(), name='view'),
]

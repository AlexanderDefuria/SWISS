from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('promotional:index'), permanent=True)),
    path('enter', views.EnterHours.as_view(), name='enter'),
    path('check/', views.validate_hours, name='check'),
    path('view', views.ViewHours.as_view(), name='view'),
]

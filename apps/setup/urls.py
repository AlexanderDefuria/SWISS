from django.urls import path, reverse
from django.views.generic import RedirectView

from . import views

app_name = 'setup'
urlpatterns = [
    path('', views.Setup.as_view(), name='setup'),
    path('change-event/', views.ChangeEvent.as_view(), name='change-event'),
    path('change-event/write', views.change_event_write, name='change-event-write'),
    path('admin/entry/team', RedirectView.as_view(url='/admin/entry/team'), name='admin-team'),
    path('admin/entry/match', RedirectView.as_view(url='/admin/entry/match'), name='admin-match')

]

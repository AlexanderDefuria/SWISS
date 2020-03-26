from django.urls import path

from . import views

app_name = 'setup'
urlpatterns = [
    path('', views.Setup.as_view(), name='setup'),
    path('change-event/', views.ChangeEvent.as_view(), name='change-event'),
    path('change-event/write', views.change_event_write, name='change-event-write')
]

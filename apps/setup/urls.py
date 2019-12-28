from django.urls import path

from . import views

app_name = 'setup'
urlpatterns = [
    path('', views.Setup.as_view(), name='team_list'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('enter', views.ViewHours.as_view(), name='enter'),
    path('view', views.EnterHours.as_view(), name='view'),
]

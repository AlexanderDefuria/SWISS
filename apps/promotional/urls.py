from django.conf.urls.static import static
from django.urls import path
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),

]

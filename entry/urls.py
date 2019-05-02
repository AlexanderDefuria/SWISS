from django.urls import path

from . import views

app_name = 'entry'
urlpatterns = [
    path('', views.TeamNumberList.as_view(), name='team_list'),
    path('<slug:pk>/auto', views.Auto.as_view(), name='auto'),
    path('<slug:pk>/auto/submit', views.write_cargo, name='write_cargo'),

]
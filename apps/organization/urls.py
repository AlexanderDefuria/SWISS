from django.urls import path

from apps.organization import views

urlpatterns = [
    path('logout/', views.logout, name='logout'),
    path('login/', views.Login.as_view(), name='login'),
    path('register/', views.Registration.as_view(), name='register'),
]
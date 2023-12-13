from django.urls import path

from apps.organization import views

urlpatterns = [
    path('logout/', views.logout, name='logout'),
    path('login/', views.Login.as_view(), name='login'),
    path('register/', views.Registration.as_view(), name='register'),
    path('management/', views.Management.as_view(), name='management'),
    path('management/matches/', views.UserList.as_view(), name='match_list'),
    path('management/matches/<int:pk>/', views.UserDetail.as_view(), name='match_detail'),
    path('management/users/', views.UserList.as_view(), name='user_list'),
    path('management/users/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
]
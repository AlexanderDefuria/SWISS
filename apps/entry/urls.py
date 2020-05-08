from django.conf.urls.static import static
from django.urls import path
from django.conf import settings

from . import views


urlpatterns = [
    path('', views.Index.as_view(), name='index'),

    path('matchscout/', views.MatchScoutLanding.as_view(), name='match_scout_landing'),
    path('matchscout/<slug:pk>/', views.MatchScout.as_view(), name='match_scout'),
    path('matchscout/<slug:pk>/check/', views.validate_match_scout, name='validate_match_scout'),
    path('matchscout/<slug:pk>/submit/', views.match_scout_submit, name='write_match_scout'),

    path('pitscout/', views.PitScoutLanding.as_view(), name='pit_scout_landing'),
    path('pitscout/<slug:pk>/', views.PitScout.as_view(), name='pit_scout'),
    path('pitscout/<slug:pk>/check/', views.validate_pit_scout, name='validate_pit_scout'),
    path('pitscout/<slug:pk>/submit/', views.pit_scout_submit, name='write_pit_scout'),

    path('visual/', views.Visualize.as_view(), name='visualize'),
    path('visual/update/', views.update_graph, name='update_graph'),
    path('visual/update/fields', views.update_fields, name='update_fields'),

    path('glance/', views.GlanceLanding.as_view(), name='glance'),
    path('glance/<slug:pk>/', views.Glance.as_view(), name='glance'),
    path('download/', views.download, name='download'),
    path('upload/', views.Upload.as_view(), name='upload'),
    path('upload/submit/', views.write_image_upload, name='upload_submit'),
    path('teams/', views.TeamList.as_view(), name='teams'),
    path('stats/', views.TeamList.as_view(), name='stats'),
    path('data/', views.Data.as_view(), name='data'),
    path('schedule/', views.ScheduleView.as_view(), name='schedule'),
    path('experimental/', views.Experimental.as_view(), name='experimental'),
    path('about/', views.About.as_view(), name='about'),
    path('settings/', views.About.as_view(), name='settings'),
    path('experimental/getcsv/', views.get_csv_ajax, name='getcsv'),

    path('logout/', views.logout, name='logout'),
    path('login/', views.login, name='login'),
]

# ----- 2019 ------
# urlpatterns = [
#     path('', views.TeamNumberList.as_view(), name='team_list'),
#     path('<slug:pk>/auto/', views.Auto.as_view(), name='auto'),
#     path('<slug:pk>/auto/check/', views.validate_match, name='validate_match'),
#     path('<slug:pk>/auto/submit/', views.write_auto, name='write_auto'),
#     path('<slug:pk>/teleop/<slug:match_number>', views.Teleop.as_view(), name='teleop'),
#     path('<slug:pk>/teleop/', views.write_teleop, name='write_teleop'),
#     path('visual/', views.Visualize.as_view(), name='visualize'),
#     path('visual/update/', views.update_graph, name='update_graph'),
#     path('visual/update/fields', views.update_fields, name='update_fields'),
#     path('download/', views.download, name='download'),
#     path('schedule/', views.ScheduleView.as_view(), name='schedule'),
#     path('image_upload/', views.ImageUpload.as_view(), name='image_upload'),
#     path('image_upload/submit', views.write_image_upload, name='write_image_upload'),
#     path('image_viewer/', views.ImageViewer.as_view(), name='image_viewer'),
#     path('pit_upload/', views.PitUpload.as_view(), name='pit_upload'),
#     path('logout/', views.logout, name='logout'),
#     path('login/', views.login, name='login'),
#
# ]

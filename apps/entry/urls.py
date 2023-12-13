from django.urls import path

from apps.entry.views import views, scout, stats, ajax

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('matchscout/', scout.MatchScoutLanding.as_view(), name='match_scout_landing'),
    path('matchscout/<slug:pk>/', scout.MatchScout.as_view(), name='match_scout'),
    path('pitscout/', scout.PitScoutLanding.as_view(), name='pit_scout_landing'),
    path('pitscout/<slug:pk>/', scout.PitScout.as_view(), name='pit_scout'),
    path('visual/', stats.Visualize.as_view(), name='visualize'),
    path('visual/update/', ajax.update_graph, name='update_graph'),
    path('visual/update/fields', ajax.update_fields, name='update_fields'),
    path('glance/', stats.GlanceLanding.as_view(), name='glance_landing'),
    path('glance/<slug:pk>/', stats.Glance.as_view(), name='glance'),
    path('glance/<slug:pk>/update/', ajax.update_glance, name='glance_update'),
    path('download/', views.download, name='download'),
    path('upload/', views.Upload.as_view(), name='upload'),
    path('upload/submit/', views.write_image_upload, name='upload_submit'),
    path('teams/', views.TeamList.as_view(), name='teams'),
    path('stats/', views.TeamList.as_view(), name='stats'),
    path('matchdata/', stats.MatchData.as_view(), name='match_data'),
    path('pitdata/', stats.PitData.as_view(), name='pit_data'),
    path('schedule/', stats.ScheduleView.as_view(), name='schedule'),
    path('schedule/all/', stats.ScheduleView.as_view(show_completed=True), name='schedule_all'),
    path('schedule/details/<slug:pk>/', stats.ScheduleDetails.as_view(), name='schedule_details'),
    path('experimental/', views.Experimental.as_view(), name='experimental'),
    path('about/', views.About.as_view(), name='about'),
    path('settings/', views.Settings.as_view(), name='settings'),
    path('experimental/getcsv/', ajax.get_csv_ajax, name='getcsv'),
    path('tutorial/', views.Tutorial.as_view(), name='tutorial'),
    path('welcome/', views.Welcome.as_view(), name='welcome'),
    path('import/', views.Import.as_view(), name='import_from_first'),
    path('admin_redirect/<str:whereto>', views.admin_redirect, name='admin_redirect'),
    path('admin_redirect/', views.admin_redirect, name='admin_redirect'),
    path('team_settings_not_found_error/', views.TeamSettingsNotFoundError.as_view(), name='team_settings_not_found_error'),
    path('frc/', views.FRCdata.as_view(), name='frc')
]

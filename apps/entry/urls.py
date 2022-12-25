from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),

    path('matchscout/', views.MatchScoutLanding.as_view(), name='match_scout_landing'),
    path('matchscout/<slug:pk>/', views.MatchScout.as_view(), name='match_scout'),
    # TODO Deprecated vv
    # path('matchscout/<slug:pk>/check/', views.validate_match_scout, name='validate_match_scout'),
    # path('matchscout/<slug:pk>/submit/', views.match_scout_submit, name='write_match_scout'),

    path('pitscout/', views.PitScoutLanding.as_view(), name='pit_scout_landing'),
    path('pitscout/<slug:pk>/', views.PitScout.as_view(), name='pit_scout'),
    path('pitscout/<slug:pk>/check/', views.validate_pit_scout, name='validate_pit_scout'),
    path('pitscout/<slug:pk>/submit/', views.pit_scout_submit, name='write_pit_scout'),

    path('visual/', views.Visualize.as_view(), name='visualize'),
    path('visual/update/', views.update_graph, name='update_graph'),
    path('visual/update/fields', views.update_fields, name='update_fields'),

    path('glance/', views.GlanceLanding.as_view(), name='glance_landing'),
    path('glance/<slug:pk>/', views.Glance.as_view(), name='glance'),
    path('glance/<slug:pk>/update/', views.update_glance, name='glance_update'),
    path('download/', views.download, name='download'),
    path('upload/', views.Upload.as_view(), name='upload'),
    path('upload/submit/', views.write_image_upload, name='upload_submit'),
    path('teams/', views.TeamList.as_view(), name='teams'),
    path('stats/', views.TeamList.as_view(), name='stats'),
    path('matchdata/', views.MatchData.as_view(), name='match_data'),
    path('pitdata/', views.PitData.as_view(), name='pit_data'),
    path('schedule/', views.ScheduleView.as_view(), name='schedule'),
    path('schedule/all/', views.ScheduleView.as_view(show_completed=True), name='schedule_all'),
    path('schedule/details/<slug:pk>/', views.ScheduleDetails.as_view(), name='schedule_details'),
    path('experimental/', views.Experimental.as_view(), name='experimental'),
    path('about/', views.About.as_view(), name='about'),
    path('settings/', views.Settings.as_view(), name='settings'),
    path('experimental/getcsv/', views.get_csv_ajax, name='getcsv'),
    path('tutorial/', views.Tutorial.as_view(), name='tutorial'),
    path('welcome/', views.Welcome.as_view(), name='welcome'),
    path('import/submit/', views.import_from_first, name='import_from_first'),
    path('import/', views.Import.as_view(), name='import'),
    path('import/schedule/submit', views.import_schedule_from_first, name='import_schedule_from_first'),

    path('logout/', views.logout, name='logout'),
    path('login/', views.login, name='login'),
    path('register/', views.Registration.as_view(), name='register'),
    path('register/check/', views.validate_registration, name='validate_register'),

    path('admin_redirect/<str:whereto>', views.admin_redirect, name='admin_redirect'),
    path('admin_redirect/', views.admin_redirect, name='admin_redirect'),

    path('team_settings_not_found_error/', views.TeamSettingsNotFoundError.as_view(), name='team_settings_not_found_error'),
]

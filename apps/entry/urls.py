from django.conf.urls.static import static
from django.urls import path
from django.conf import settings

from . import views

app_name = 'entry'
urlpatterns = [
    path('', views.TeamNumberList.as_view(), name='team_list'),
    path('<slug:pk>/auto/', views.Auto.as_view(), name='auto'),
    path('<slug:pk>/auto/check/', views.validate_match, name='validate_match'),
    path('<slug:pk>/auto/submit/', views.write_auto, name='write_auto'),
    path('<slug:pk>/teleop/<slug:match_number>', views.Teleop.as_view(), name='teleop'),
    path('<slug:pk>/teleop/', views.write_teleop, name='write_teleop'),
    path('visual/', views.Visualize.as_view(), name='visualize'),
    path('visual/update/', views.update_graph, name='update_graph'),
    path('download/', views.download, name='download'),
    path('schedule/', views.ScheduleView.as_view(), name='schedule'),
    path('image_upload/', views.ImageUpload.as_view(), name='image_upload'),
    path('image_upload/submit', views.write_image_upload, name='write_image_upload'),
    path('image_viewer/', views.ImageViewer.as_view(), name='image_viewer'),
    path('pit_upload/', views.PitUpload.as_view(), name='pit_upload')
]

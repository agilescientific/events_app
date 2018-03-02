from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('event/<int:pk>', views.EventDetailView.as_view(), name='event-detail'),
    path('event/<int:pk>/join', views.JoinEventView.as_view(), name='event-join'),
    path('event/<int:pk>/participants', views.ParticipantListView.as_view(), name='event-participants'),
    path('event/<int:pk>/teams', views.TeamListView.as_view(), name='event-teams'),
    path('event/<int:pk>/create_team', views.CreateTeamView.as_view(), name='event-createteam'),
    path('team/<int:pk>', views.TeamDetailView.as_view(), name='team-detail'),
]
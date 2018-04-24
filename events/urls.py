from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('event/<slug:slug>', views.EventDetailView.as_view(), name='event-detail'),
    path('event/<slug:slug>/join', views.JoinEventView.as_view(), name='event-join'),
    path('event/<slug:slug>/participants', views.ParticipantListView.as_view(), name='event-participants'),
    path('event/<slug:slug>/teams', views.TeamListView.as_view(), name='event-teams'),
    path('event/<slug:slug>/forum', views.ForumView.as_view(), name='event-forum'),
    path('event/<slug:slug>/projects', views.ProjectListView.as_view(), name='event-projects'),
    path('event/<slug:slug>/create_team', views.CreateTeamView.as_view(), name='event-createteam'),
    path('event/<slug:slug>/create_project', views.CreateProjectView.as_view(), name='event-createproject'),
    path('team/<int:pk>', views.TeamDetailView.as_view(), name='team-detail'),
    path('project/<slug:slug>', views.ProjectDetailView.as_view(), name='project-detail'),
    path('project/<slug:slug>/edit', views.ProjectEditView.as_view(), name='project-edit'),
] 
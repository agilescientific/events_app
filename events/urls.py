from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('event/<int:pk>', views.EventDetailView.as_view(), name='event-detail'),
    path('event/<int:pk>/join', views.JoinEventView.as_view(), name='event-join'),
    path('event/<int:pk>/participants', views.ParticipantListView.as_view(), name='event-participants'),
    path('event/<int:pk>/teams', views.TeamListView.as_view(), name='event-teams'),
    path('event/<int:pk>/forum', views.ForumView.as_view(), name='event-forum'),
    path('event/<int:pk>/projects', views.ProjectListView.as_view(), name='event-projects'),
    path('event/<int:pk>/create_team', views.CreateTeamView.as_view(), name='event-createteam'),
    path('event/<int:pk>/create_project', views.CreateProjectView.as_view(), name='event-createproject'),
    path('team/<int:pk>', views.TeamDetailView.as_view(), name='team-detail'),
    path('project/<int:pk>', views.ProjectDetailView.as_view(), name='project-detail'),
    path('project/<int:pk>/edit', views.ProjectEditView.as_view(), name='project-edit'),
] 
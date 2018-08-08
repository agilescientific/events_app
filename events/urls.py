from django.urls import path, re_path
from rest_framework import routers
from django.conf.urls import url, include

from . import views

# router = routers.DefaultRouter()
# router.register(r'ideas', views.IdeaViewSet)
# router.register(r'events', views.EventViewSet)
# router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('event/<slug:slug>', views.EventDetailView.as_view(), name='event-detail'),
    path('event/<slug:slug>/join', views.JoinEventView.as_view(), name='event-join'),
    path('event/<slug:slug>/participants', views.ParticipantListView.as_view(), name='event-participants'),
    # path('event/<slug:slug>/teams', views.TeamListView.as_view(), name='event-teams'),
    path('event/<slug:slug>/forum', views.ForumView.as_view(), name='event-forum'),
    path('event/<slug:slug>/projects', views.ProjectListView.as_view(), name='event-projects'),
    path('event/<slug:slug>/rules', views.RulesView.as_view(), name='event-rules'),
    path('event/<slug:slug>/ideas', views.IdeasView.as_view(), name='event-ideas'),
    path('event/<slug:slug>/getideas', views.GetIdeas.as_view(), name='event-getideas'),
    # path('event/<slug:slug>/create_team', views.CreateTeamView.as_view(), name='event-createteam'),
    path('event/<slug:slug>/create_project', views.CreateProjectView.as_view(), name='event-createproject'),
    path('event/<slug:slug>/create_idea', views.CreateIdeaView.as_view(), name='event-createidea'),
    path('event/<slug:slug>/vote_idea', views.VoteIdea.as_view(), name='event-voteidea'),
    path('organization/<slug:slug>', views.OrganizationDetailView.as_view(), name='organization-detail'),
    path('project/<slug:slug>', views.ProjectDetailView.as_view(), name='project-detail'),
    path('project/<slug:slug>/edit', views.ProjectEditView.as_view(), name='project-edit'),
    path('project/<slug:slug>/delete', views.ProjectDeleteView.as_view(), name='project-delete'),
    path('project/<slug:slug>/github', views.GetGithubInfo.as_view(), name='project-github'),
    path('organization/<slug:slug>/upload_pic/', views.UploadPicture.as_view(), name='upload_pic'),
    path('terms', views.TermsView.as_view(), name='terms'),
    path('privacy', views.PrivacyView.as_view(), name='privacy'),
    # path('event/<slug:slug>/mforum', views.MForumView.as_view(), name='machinita'),
    # url(r'^', include(router.urls)),
] 
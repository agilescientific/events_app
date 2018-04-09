from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse

from django.contrib.auth import get_user_model
User = get_user_model()

from .models import Event, EventRegistration, Team, Project, EventClass
from .forms import TeamForm, ProjectForm

from urllib.parse import urlparse
# Create your views here.

class IndexView(ListView):
    template_name = "index.html"
    model = Event
    context_object_name = 'events'

class EventDetailView(DetailView):
    template_name = "eventDetail.html"
    model = Event
    context_object_name = 'event'

    def get_context_data(self,**kwargs):
        context = super(EventDetailView, self).get_context_data(**kwargs)
        q_reg = len(EventRegistration.objects.filter(member_id = self.request.user.id,
                                                     event_id = self.kwargs['pk']))
        if q_reg > 0:
            context['registered'] = True
        else:
            context['registered'] = False

        return context

class ParticipantListView(ListView):
    template_name = "participantList.html"
    # model = EventRegistration
    queryset = EventRegistration.objects
    context_object_name = 'participants'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.participants = queryset.filter(event_id = self.kwargs['pk'])
        return self.participants

    def get_context_data(self,**kwargs):
        context = super(ParticipantListView, self).get_context_data(**kwargs)
        context['event'] = Event.objects.filter(id = self.kwargs['pk'])[0]

        return context

class TeamListView(ListView):
    template_name = "teamList.html"
    # model = EventRegistration
    queryset = Team.objects
    context_object_name = 'teams'

    def render_to_response(self, context):
        event_pk = self.kwargs['pk']
        event_obj = Event.objects.get(id=event_pk)
        if str(event_obj.event_class) != 'hackathon':
            return HttpResponseRedirect('/event/{}'.format(event_pk))

        return super(TeamListView, self).render_to_response(context)

    def get_queryset(self):
        queryset = super().get_queryset()
        self.teams = queryset.filter(event_id = self.kwargs['pk'])
        return self.teams

    def get_context_data(self,**kwargs):
        context = super(TeamListView, self).get_context_data(**kwargs)
        context['event'] = Event.objects.filter(id = self.kwargs['pk'])[0]
        q_reg = len(EventRegistration.objects.filter(member_id = self.request.user.id,
                                                     event_id = self.kwargs['pk']))
        if q_reg > 0:
            context['registered'] = True
        else:
            context['registered'] = False

        return context

class ProjectListView(ListView):
    template_name = "projectList.html"
    queryset = Project.objects
    context_object_name = 'projects'

    def render_to_response(self, context):
        event_pk = self.kwargs['pk']
        event_obj = Event.objects.get(id=event_pk)
        if str(event_obj.event_class) != 'projects':
            return HttpResponseRedirect('/event/{}'.format(event_pk))

        return super(ProjectListView, self).render_to_response(context)

    def get_queryset(self):
        queryset = super().get_queryset()
        self.projects = queryset.filter(event_id = self.kwargs['pk'])
        return self.projects

    def get_context_data(self,**kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        context['event'] = Event.objects.filter(id = self.kwargs['pk'])[0]
        q_reg = len(EventRegistration.objects.filter(member_id = self.request.user.id,
                                                     event_id = self.kwargs['pk']))
        if q_reg > 0:
            context['registered'] = True
        else:
            context['registered'] = False

        return context

class JoinEventView(LoginRequiredMixin, View):
    login_url = '/account/login/'
    model = Event

    def get(self, request, *args, **kwargs):
        event_pk = self.kwargs['pk']
        obj, created = EventRegistration.objects.get_or_create(
                        event = Event.objects.get(id=event_pk),
                        member = User.objects.get(id=self.request.user.id),
                        )
        return HttpResponseRedirect('/event/{}'.format(event_pk))

class CreateTeamView(FormView):
    template_name = 'teamRegistration.html'
    model = Team
    form_class = TeamForm
    success_url = '/'

    def get_form(self, form_class=form_class):
        """
        Check if the user has already filled in the form.
        If so, then show the form populated with those answers,
        to let user change them.
        """
        try:
            team = Team.objects.get(leader=self.request.user, event=self.kwargs['pk'])
            return form_class(instance=team, **self.get_form_kwargs())
        except Team.DoesNotExist:
            return form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        event_pk = self.kwargs['pk']
        self.object = form.save(commit=False)
        self.object.leader = self.request.user
        self.object.event = Event.objects.get(id=event_pk)
        self.object.save()
        form.save_m2m()
        self.object.members.add(self.request.user)

        self.success_url = '/event/{}/teams'.format(event_pk)
        return super().form_valid(form)

    def get_context_data(self,**kwargs):
        context = super(CreateTeamView, self).get_context_data(**kwargs)
        context['event'] = Event.objects.filter(id = self.kwargs['pk'])[0]
        context['creator'] = self.request.user
        return context

class CreateProjectView(LoginRequiredMixin, FormView):
    template_name = 'projectRegistration.html'
    model = Project
    form_class = ProjectForm
    success_url = '/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        event_pk = self.kwargs['pk']
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        self.object.event = Event.objects.get(id=event_pk)
        self.object.save()
        form.save_m2m()
        self.success_url = '/event/{}/projects'.format(event_pk)
        return super().form_valid(form)

    def get_context_data(self,**kwargs):
        context = super(CreateProjectView, self).get_context_data(**kwargs)
        context['event'] = Event.objects.filter(id = self.kwargs['pk'])[0]
        context['creator'] = self.request.user
        return context

class TeamDetailView(DetailView):
    template_name = "teamDetail.html"
    model = Team
    context_object_name = 'team'

    def get_context_data(self,**kwargs):
        context = super(TeamDetailView, self).get_context_data(**kwargs)
        context['event'] = Event.objects.get(id = context['team'].event.id)

        return context

class ProjectDetailView(DetailView):
    template_name = "projectDetail.html"
    model = Project
    context_object_name = 'project'

    def get_context_data(self,**kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['event'] = Event.objects.get(id = context['project'].event.id)

        return context
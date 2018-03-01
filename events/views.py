from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
User = get_user_model()

from .models import Event, EventRegistration, Team
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

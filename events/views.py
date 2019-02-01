from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from machina.apps.forum.views import ForumView as BaseForumView
from machina.apps.forum.views import Forum
import datetime
from .models import Event, EventRegistration, Organization, Project,\
                    EventClass, Idea, IdeaComment, GitHubCache
from .forms import OrganizationForm, ProjectForm, ImageUploadForm, IdeaForm
from urllib.parse import urlparse
from markdownx.utils import markdownify
import requests
import json
from django.http import Http404

import numpy as np
import os
from subprocess import Popen, PIPE, STDOUT
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Getting ready for JS frontend
from django.core import serializers
from rest_framework import viewsets
from .serializers import IdeaSerializer, EventSerializer, UserSerializer

User = get_user_model()

class IndexView(ListView):
    template_name = "index.html"
    model = Event
    context_object_name = 'events'

    # def get_context_data(self, **kwargs):
    #     context = super(IndexView, self).get_context_data(**kwargs)
    #     now = datetime.datetime.now()
    #     events = self.model.objects.all()
    #     upcoming_e = events.filter(event_startdate__gte=now)
    #     past_e = events.exclude(event_startdate__gte=now)
    #     context['past_e'] = past_e
    #     context['upcoming_e'] = upcoming_e    
    #     print(upcoming_e)
    #     return context

class ForumView(LoginRequiredMixin, DetailView):
    template_name = "forum.html"
    model = Event
    context_object_name = 'event'

    def get_context_data(self,**kwargs):
        context = super(ForumView, self).get_context_data(**kwargs)
        context['current'] = 'forum'

        return context

class EventDetailView(DetailView):
    template_name = "eventDetail.html"
    model = Event
    context_object_name = 'event'

    def get_context_data(self,**kwargs):
        context = super(EventDetailView, self).get_context_data(**kwargs)
        pk = Event.objects.get(slug = self.kwargs['slug']).id
        q_reg = len(EventRegistration.objects.filter(member_id = self.request.user.id,
                                                     event_id = pk))
        if q_reg > 0:
            context['registered'] = True
        else:
            context['registered'] = False

        context['current'] = 'description'
        context['html_body'] = markdownify(Event.objects.get(slug = self.kwargs['slug']).body_text)
        return context

class ParticipantListView(ListView):
    template_name = "participantList.html"
    # model = EventRegistration
    queryset = EventRegistration.objects
    context_object_name = 'participants'

    def get_queryset(self):
        queryset = super().get_queryset()
        pk = Event.objects.get(slug = self.kwargs['slug']).id
        self.participants = queryset.filter(event_id = pk).exclude(member_id=1)
        return self.participants

    def get_context_data(self,**kwargs):
        context = super(ParticipantListView, self).get_context_data(**kwargs)
        context['event'] = Event.objects.get(slug = self.kwargs['slug'])
        context['current'] = 'participants'
        return context

class OrganizationListView(ListView):
    template_name = "organizationList.html"
    # model = EventRegistration
    queryset = Organization.objects
    context_object_name = 'teams'

    def render_to_response(self, context):
        event_obj = Event.objects.get(slug = self.kwargs['slug'])
        if str(event_obj.event_class) != 'hackathon':
            return HttpResponseRedirect('/event/{}'.format(self.kwargs['slug']))

        return super(OrganizationListView, self).render_to_response(context)

    def get_queryset(self):
        queryset = super().get_queryset()
        event_pk = Event.objects.get(slug = self.kwargs['slug']).id
        self.teams = queryset.filter(event_id = event_pk)
        return self.teams

    def get_context_data(self,**kwargs):
        context = super(OrganizationListView, self).get_context_data(**kwargs)
        event_pk = Event.objects.get(slug = self.kwargs['slug']).id
        context['event'] = Event.objects.get(slug = self.kwargs['slug'])
        q_reg = len(EventRegistration.objects.filter(member_id = self.request.user.id,
                                                     event_id = event_pk))
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
        event_pk = Event.objects.get(slug = self.kwargs['slug']).id
        event_obj = Event.objects.get(id=event_pk)
        if str(event_obj.event_class) != 'projects':
            return HttpResponseRedirect('/event/{}'.format(event_obj.slug))

        return super(ProjectListView, self).render_to_response(context)

    def get_queryset(self):
        queryset = super().get_queryset()
        pk = Event.objects.get(slug = self.kwargs['slug']).id
        self.projects = queryset.filter(event_id = pk)
        return self.projects

    def get_context_data(self,**kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        pk = Event.objects.get(slug = self.kwargs['slug']).id
        context['event'] = Event.objects.get(id = pk)
        q_reg = len(EventRegistration.objects.filter(member_id = self.request.user.id,
                                                     event_id = pk))
        if q_reg > 0:
            context['registered'] = True
        else:
            context['registered'] = False
        context['current'] = 'projects'
        return context

class ZooDashView(ListView):
    template_name = "githubDash.html"
    queryset = Project.objects
    context_object_name = 'projects'

    def render_to_response(self, context):
        event_pk = Event.objects.get(slug = self.kwargs['slug']).id
        event_obj = Event.objects.get(id=event_pk)
        if str(event_obj.event_class) != 'projects':
            return HttpResponseRedirect('/event/{}'.format(event_obj.slug))

        return super(ZooDashView, self).render_to_response(context)

    def get_queryset(self):
        queryset = super().get_queryset()
        pk = Event.objects.get(slug = self.kwargs['slug']).id
        self.projects = queryset.filter(event_id = pk)
        return self.projects

    def get_context_data(self,**kwargs):
        context = super(ZooDashView, self).get_context_data(**kwargs)
        pk = Event.objects.get(slug = self.kwargs['slug']).id
        context['event'] = Event.objects.get(id = pk)
        q_reg = len(EventRegistration.objects.filter(member_id = self.request.user.id,
                                                     event_id = pk))
        if q_reg > 0:
            context['registered'] = True
        else:
            context['registered'] = False
        context['current'] = 'custom'
        context['custom'] = 'Dashboard'
        return context

class JoinEventView(LoginRequiredMixin, View):
    login_url = '/account/login/'
    model = Event

    def get(self, request, *args, **kwargs):
        event_pk = Event.objects.get(slug = self.kwargs['slug']).id
        obj, created = EventRegistration.objects.get_or_create(
                        event = Event.objects.get(id=event_pk),
                        member = User.objects.get(id=self.request.user.id),
                        )
        return HttpResponseRedirect('/event/{}'.format(self.kwargs['slug']))

class CreateOrganizationView(FormView):
    template_name = 'organizationRegistration.html'
    model = Organization
    form_class = OrganizationForm
    success_url = '/'

    def get_form(self, form_class=form_class):
        """
        Check if the user has already filled in the form.
        If so, then show the form populated with those answers,
        to let user change them.
        """
        try:
            pk = Event.objects.get(slug = self.kwargs['slug']).id
            organization = Organization.objects.get(leader=self.request.user)
            return form_class(instance=team, **self.get_form_kwargs())
        except Organization.DoesNotExist:
            return form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        event_pk = Event.objects.get(slug = self.kwargs['slug']).id
        self.object = form.save(commit=False)
        self.object.leader = self.request.user
        self.object.event = Event.objects.get(id=event_pk)
        self.object.save()
        form.save_m2m()
        self.object.members.add(self.request.user)

        self.success_url = '/organization/{}'.format(self.kwargs['slug'])
        return super().form_valid(form)

    def get_context_data(self,**kwargs):
        context = super(CreateOrganizationView, self).get_context_data(**kwargs)
        context['event'] = Event.objects.get(slug = self.kwargs['slug'])
        context['creator'] = self.request.user
        return context

def notify_slack(m, l=None, swhook=settings.SLACK_WEBHOOK):
    """
    Setup webhook for Slack
    """
    if l != None:
        link = "<{}|Click here> for details".format(l)
        message = "{} {}".format(m, link)
    else:
        message = m

    payload = {'text':message}
    r = requests.post(swhook, json=payload)
    print(r.text)
    
    return

class CreateProjectView(LoginRequiredMixin, FormView):
    template_name = 'projectRegistration.html'
    model = Project
    form_class = ProjectForm
    success_url = '/'
    # fields = ['name', 'members', 'detail_small', 'detail_long', 'main_url', 'resources', 'github']

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super(CreateProjectView, self).get_initial()

        if 'from' in self.request.GET:
            try:
                idea = Idea.objects.get(slug=self.request.GET['from'])
                initial['name'] = idea.name
                initial['detail_small'] = idea.detail_short
                initial['detail_long'] = idea.detail
            except:
                pass

        return initial

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        self.success_url = '/event/{}/projects'.format(self.kwargs['slug'])
        if 'cancel' in self.request.POST:
            return HttpResponseRedirect(self.get_success_url())

        event = Event.objects.get(slug = self.kwargs['slug'])
        event_pk = event.id
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        self.object.event = Event.objects.get(id=event_pk)
        self.object.save()
        form.save_m2m()

        # Slack notify:
        message = "Project *{}* was created.".format(self.object.name)
        link = settings.SITE_URL + "/project/{}".format(self.object.slug)
        swhook = event.slack_webhook
        if swhook:
            notify_slack(message, link, swhook)
        
        return super().form_valid(form)

    def get_context_data(self,**kwargs):
        context = super(CreateProjectView, self).get_context_data(**kwargs)
        context['event'] = Event.objects.get(slug = self.kwargs['slug'])
        context['creator'] = self.request.user
        return context

class ProjectEditView(LoginRequiredMixin, FormView):
    template_name = 'projectEdit.html'
    model = Project
    form_class = ProjectForm
    success_url = '/'
    context_object_name = 'project'

    def get_form(self, form_class=form_class):
        """
        Check if the user has already filled in the form.
        If so, then show the form populated with those answers,
        to let user change them.
        """
        project = get_object_or_404(Project, creator=self.request.user, slug=self.kwargs['slug'])
        return form_class(instance=project, **self.get_form_kwargs())
        # try:
        #     project = Project.objects.get(creator=self.request.user, id=self.kwargs['pk'])
        #     return form_class(instance=project, **self.get_form_kwargs())
        # except Project.DoesNotExist:
        #     return form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        proj = Project.objects.get(slug=self.kwargs['slug'])
        event = Event.objects.get(id = proj.event_id)
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        self.object.event = event
        self.object.save()
        form.save_m2m()
        self.success_url = '/project/{}'.format(self.kwargs['slug'])
        return super().form_valid(form)

    def get_context_data(self,**kwargs):
        context = super(ProjectEditView, self).get_context_data(**kwargs)
        proj = Project.objects.get(slug=self.kwargs['slug'])
        events = Event.objects.filter(id = proj.event_id)
        if (len(events)>0):
            context['event'] = events[0]
        context['creator'] = self.request.user
        context['pslug'] = self.kwargs['slug']
        return context

class ProjectDeleteView(DeleteView):
    """
    Sub-class the DeleteView to restrict a User from deleting other 
    user's data.
    """
    template_name = 'projectDelete.html'
    model = Project
    success_message = "Deleted Successfully"

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(ProjectDeleteView, self).get_object()
        if not obj.creator == self.request.user:
            raise Http404
        return obj

    def get_success_url(self):
        eslug = Event.objects.get(id = self.object.event_id).slug
        return reverse('event-projects', kwargs={'slug':eslug})

    def get_context_data(self,**kwargs):
        context = super(ProjectDeleteView, self).get_context_data(**kwargs)
        proj = Project.objects.get(slug=self.kwargs['slug'])
        event = Event.objects.get(id = proj.event_id)
        context['event'] = event
        context['eslug'] = self.kwargs['slug']
        return context

class OrganizationDetailView(DetailView):
    template_name = "organizationDetail.html"
    model = Organization
    context_object_name = 'team'

    def get_context_data(self,**kwargs):
        context = super(OrganizationDetailView, self).get_context_data(**kwargs)

        return context

class ProjectDetailView(DetailView):
    template_name = "projectDetail.html"
    model = Project
    context_object_name = 'project'

    def get_context_data(self,**kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['event'] = Event.objects.get(id = context['project'].event.id)
        context['html_body'] = markdownify(self.object.detail_long)

        return context

class UploadPicture(LoginRequiredMixin, View):

    def post(self, request, slug):
        if request.method == 'POST':
            form = ImageUploadForm(request.POST, request.FILES)
            if form.is_valid():
                m = Organization.objects.get(slug=slug)
                m.org_logo = form.cleaned_data['image']
                m.save()
                return HttpResponseRedirect('/organization/{}'.format(slug))
        return HttpResponseRedirect('/organization/{}'.format(slug))

class GetGithubInfo(View):

    def get(self, request, slug):
        if request.method == 'GET':
            json_r = {}
            proj = get_object_or_404(Project, slug=slug)
            if proj.github != '' or proj.github != None:
                payload = {'client_id':settings.GH_ID, 'client_secret':settings.GH_SECRET}

                repostr = urlparse(proj.github).path
                
                if repostr[-1]=='/': repostr[:-1]

                repo_url = 'https://api.github.com/repos'+ repostr
                
                issues_r = requests.get(repo_url, params=payload)
                if issues_r.status_code == 200:
                    if issues_r.json()['has_issues']:
                        issues_r = requests.get(repo_url+'/issues', params=payload)
                        json_r = issues_r.json()
                    else:
                        json_r = {}
                elif issues_r.status_code > 400:
                    json_r = {'error' : True}

                headers = {'Accept':'application/vnd.github.v3.html+json'}
                readme = requests.get(repo_url+'/readme', params=payload, headers=headers)
                if readme.status_code == 200:

                    if type(json_r) == list:
                        json_r.append({'readme_html': readme.content.decode()})
                    else:
                        json_r['readme_html'] = readme.content.decode()

                    contents_r = requests.get(repo_url+'/contents/', params=payload)
                    contents_json = contents_r.json()
                    json_r.append({'files': contents_json})
                elif issues_r.status_code > 400:
                    json_r = {'error' : True}

        return JsonResponse(json_r, safe=False)

class GetZooGithubInfo(View):

    def get(self, request, slug):
        if request.method == 'GET':

            repro_git = GitHubCache.objects.get(id=1)
            json_r = json.loads(repro_git.content)
            days = [1, 2 ,3]                
            stats = np.array(json_r[-1]['day_stats'])
            # stats = [ x[2] for x in list(json_r[-1]['day_stats'])]
            acc = []
            for day in days:
                acc.append(int(np.sum(stats[stats[:,0] == day][:,2])))

            # hours = list(range(0, len(stats)))
            days = ['Monday', 'Tuesday', 'Wednesday']
            json_r.append({'x': days})
            json_r.append({'y': acc})

        return JsonResponse(json_r, safe=False)

class TermsView(TemplateView):
    template_name = 'terms.html'

class PrivacyView(TemplateView):
    template_name = 'privacy.html'

class MForumView(BaseForumView):

    def get_forum(self):
        # self.forum = super(ForumView, self).get_forum(**kwargs)
        self.event = get_object_or_404(Event, slug=self.kwargs['slug'])
        self.forum = get_object_or_404(Forum, pk=self.event.forum_id)
        return self.forum

    def get_context_data(self, **kwargs):
        context = super(MForumView, self).get_context_data(**kwargs)
        # Some additional data can be added to the context here
        context['event'] = self.event
        return context

class RulesView(DetailView):
    template_name = "rules.html"
    model = Event
    context_object_name = 'event'

    def get_context_data(self,**kwargs):
        context = super(RulesView, self).get_context_data(**kwargs)
        context['current'] = 'rules'
        context['html_body'] = markdownify(Event.objects.get(slug = self.kwargs['slug']).rules)
        return context

class VenueView(DetailView):
    template_name = "venue.html"
    model = Event
    context_object_name = 'event'

    def get_context_data(self,**kwargs):
        context = super(VenueView, self).get_context_data(**kwargs)
        context['current'] = 'venue'
        context['html_body'] = markdownify(Event.objects.get(slug = self.kwargs['slug']).venue)
        return context

class ScheduleView(DetailView):
    template_name = "schedule.html"
    model = Event
    context_object_name = 'event'

    def get_context_data(self,**kwargs):
        context = super(ScheduleView, self).get_context_data(**kwargs)
        context['current'] = 'schedule'
        context['html_body'] = markdownify(Event.objects.get(slug = self.kwargs['slug']).schedule)
        return context

class IdeasView(DetailView):
    template_name = "ideaList.html"
    model = Event
    context_object_name = 'event'

    def get_context_data(self,**kwargs):
        context = super(IdeasView, self).get_context_data(**kwargs)
        context['cuser'] = self.request.user
        q_reg = len(EventRegistration.objects.filter(member_id = self.request.user.id,
                                                     event_id = self.object.id))
        if q_reg > 0:
            context['registered'] = True
        else:
            context['registered'] = False
        context['current'] = 'ideas'
        context['html_body'] = markdownify(Event.objects.get(slug = self.kwargs['slug']).rules)
        return context

class CreateIdeaView(LoginRequiredMixin, FormView):
    template_name = 'ideaRegistration.html'
    model = Idea
    form_class = IdeaForm
    success_url = '/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        self.success_url = '/event/{}/ideas'.format(self.kwargs['slug'])
        if 'cancel' in self.request.POST:
            return HttpResponseRedirect(self.get_success_url())

        event = Event.objects.get(slug = self.kwargs['slug'])
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        self.object.event = event
        self.object.save(commit=True)

        # Slack notify:
        message = "Idea *{}* was created.".format(self.object.name)
        link = settings.SITE_URL + '/event/{}/ideas'.format(self.kwargs['slug'])
        swhook = event.slack_webhook
        # swhook = "https://hooks.slack.com/services/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"
        if swhook:
            notify_slack(message, link, swhook)
        
        return super().form_valid(form)

    def get_context_data(self,**kwargs):
        context = super(CreateIdeaView, self).get_context_data(**kwargs)
        context['event'] = Event.objects.get(slug = self.kwargs['slug'])
        context['creator'] = self.request.user
        return context

class IdeaDetailView(DetailView):
    template_name = "ideaDetail.html"
    model = Idea
    context_object_name = 'idea'

    def get_context_data(self,**kwargs):
        context = super(IdeaDetailView, self).get_context_data(**kwargs)
        context['event'] = Event.objects.get(id = context['idea'].event.id)
        context['html_body'] = markdownify(self.object.detail)

        return context

class IdeaEditView(LoginRequiredMixin, FormView):
    template_name = 'ideaEdit.html'
    model = Idea
    form_class = IdeaForm
    success_url = '/'
    context_object_name = 'idea'

    def get_form(self, form_class=form_class):
        """
        Check if the user has already filled in the form.
        If so, then show the form populated with those answers,
        to let user change them.
        """
        idea = get_object_or_404(Idea, creator=self.request.user, slug=self.kwargs['slug'])
        return form_class(instance=idea, **self.get_form_kwargs())

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        idea = Idea.objects.get(slug=self.kwargs['slug'])
        event = Event.objects.get(id = idea.event_id)
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        self.object.event = event
        self.object.save()

        self.success_url = '/idea/{}'.format(self.kwargs['slug'])
        return super().form_valid(form)

    def get_context_data(self,**kwargs):
        context = super(IdeaEditView, self).get_context_data(**kwargs)
        idea = Idea.objects.get(slug=self.kwargs['slug'])
        events = Event.objects.filter(id = idea.event_id)
        if (len(events)>0):
            context['event'] = events[0]
        context['creator'] = self.request.user
        context['islug'] = self.kwargs['slug']
        return context

class IdeaDeleteView(DeleteView):
    """
    Sub-class the DeleteView to restrict a User from deleting other 
    user's data.
    """
    template_name = 'ideaDelete.html'
    model = Idea
    success_message = "Deleted Successfully"

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(IdeaDeleteView, self).get_object()
        if not obj.creator == self.request.user:
            raise Http404
        return obj

    def get_success_url(self):
        eslug = Event.objects.get(id = self.object.event_id).slug
        return reverse('event-ideas', kwargs={'slug':eslug})

    def get_context_data(self,**kwargs):
        context = super(IdeaDeleteView, self).get_context_data(**kwargs)
        idea = Idea.objects.get(slug=self.kwargs['slug'])
        event = Event.objects.get(id = idea.event_id)
        context['event'] = event
        context['eslug'] = self.kwargs['slug']
        return context

class GetIdeas(View):

    def get(self, request, slug):
        if request.method == 'GET':
            json_r = []
            event = get_object_or_404(Event, slug=self.kwargs['slug'])
            ideas = Idea.objects.filter(event = event.id).order_by('-votes')
            query_dict = json.loads(serializers.serialize("json", ideas))
            # query_dict = []

            for i in ideas:
                idea = {}
                idea["name"] = i.name
                idea["detail_short"] = i.detail_short
                idea["detail"] = i.detail
                idea["event"] = i.event.slug
                idea["creator"] = i.creator.username
                idea["votes"] = i.votes
                idea["voters"] = [v.username for v in i.voters.all()]
                idea["comments"] = [c.content for c in i.comments.all()]
                print(idea["comments"])
                idea["get_absolute_url"] = "/idea/"+i.slug
                json_r.append(idea)

            return HttpResponse(json.dumps(json_r), content_type='application/json')

class PostCommentIdea(View, LoginRequiredMixin):

    def post(self, request, slug):
        success_url = '/idea/{}'.format(self.kwargs['slug'])

        if request.method == 'POST':
            if 'idea' in request.POST:
                idea = Idea.objects.get(slug=self.kwargs['slug'])
                comment = IdeaComment()
                comment.author = self.request.user
                comment.content = request.POST['comment']
                comment.parentIdea = idea
                comment.event = idea.event
                comment.save()
                idea.comments.add(comment)
                idea.save()

        return HttpResponseRedirect(success_url)

class CommentDeleteView(DeleteView):
    """
    Sub-class the DeleteView to restrict a User from deleting other 
    user's data.
    """
    template_name = 'commentDelete.html'
    model = IdeaComment
    success_message = "Deleted Successfully"

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(CommentDeleteView, self).get_object()
        if not obj.author == self.request.user:
            raise Http404
        return obj

    def get_success_url(self):
        eslug = Event.objects.get(id = self.object.event_id).slug
        return reverse('idea-detail', kwargs={'slug':self.kwargs['slug']})

    def get_context_data(self,**kwargs):
        context = super(CommentDeleteView, self).get_context_data(**kwargs)
        idea = Idea.objects.get(slug=self.kwargs['slug'])
        event = Event.objects.get(id = idea.event_id)
        context['event'] = event
        context['eslug'] = self.kwargs['slug']
        return context

class DeleteCommentIdea(View, LoginRequiredMixin):

    def put(self, request, slug):
        success_url = '/idea/{}'.format(self.kwargs['slug'])

        if request.method == 'POST':
            if 'idea' in request.POST:
                idea = Idea.objects.get(slug=self.kwargs['slug'])
                comment = get_object_or_404(IdeaComment, parentIdea=idea)
                comment.delete()

        return HttpResponseRedirect(success_url)

class AddVoteIdea(View, LoginRequiredMixin):

    def post(self, request, slug):
        success_url = '/event/{}/ideas'.format(self.kwargs['slug'])

        if request.method == 'POST':
            if 'name' in request.POST:
                idea = get_object_or_404(Idea, name=request.POST['name'])
                idea.votes = idea.votes + 1
                idea.voters.add(self.request.user)
                idea.save()

        return HttpResponseRedirect(success_url)

class RemVoteIdea(View, LoginRequiredMixin):

    def post(self, request, slug):
        success_url = '/event/{}/ideas'.format(self.kwargs['slug'])

        if request.method == 'POST':
            if 'name' in request.POST:
                idea = get_object_or_404(Idea, name=request.POST['name'])
                idea.votes = idea.votes - 1
                idea.voters.remove(self.request.user)
                idea.save()
                print(idea)

        return HttpResponseRedirect(success_url)

class IdeaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Ideas to be viewed or edited.
    """
    queryset = Idea.objects.all().order_by('votes')
    serializer_class = IdeaSerializer

class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Events to be viewed or edited.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = EventSerializer

class HandleGitPush(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(HandleGitPush, self).dispatch(request, *args, **kwargs)

    def post(self, request):

        if request.method == 'POST':
            if "repository" in request.POST:
                cmd = "git clone --depth 1 ssh://git@github.com:dfcastap/apipushgo.git /tmp/apipushgo"
                # result = subprocess.call(cmd, shell=True)
                p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
                output = p.stdout.read()
                with open("/tmp/git_out",'w') as f:
                    f.write(output)

        return 200

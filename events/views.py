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
from .models import Event, EventRegistration, Organization, Project, EventClass
from .forms import OrganizationForm, ProjectForm, ImageUploadForm
from urllib.parse import urlparse
from markdownx.utils import markdownify
import requests

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
        eslug = event.slug
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

                issues_url = 'https://api.github.com/repos'+ repostr
                
                issues_r = requests.get(issues_url, json=payload)
                if issues_r.status_code == 200:
                    if issues_r.json()['has_issues']:
                        payload = {'client_id':settings.GH_ID, 'client_secret':settings.GH_SECRET}
                        issues_r = requests.get(issues_url+'/issues', json=payload)
                        json_r = issues_r.json()
                    else:
                        json_r = {}
                elif issues_r.status_code > 400:
                    json_r = {'error' : True}

                headers = {'Accept':'application/vnd.github.v3.html+json'}
                readme = requests.get(issues_url+'/readme', json=payload, headers=headers)
                if readme.status_code == 200:

                    if type(json_r) == list:
                        json_r.append({'readme_html': readme.content.decode()})
                    else:
                        json_r['readme_html'] = readme.content.decode()
                elif issues_r.status_code > 400:
                    json_r = {'error' : True}

        #return HttpResponseRedirect('/project/{}'.format(slug))
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
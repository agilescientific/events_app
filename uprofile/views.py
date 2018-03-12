from django.shortcuts import render, get_object_or_404

from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
import account.views
from account.utils import default_redirect
import datetime
from django.views.generic import DetailView, ListView

from .forms import SettingsForm

from django.contrib.auth import get_user_model
User = get_user_model()

from .models import UProfile
from events.models import Team, EventRegistration
from django.db.models import Q


class SettingsView(account.views.SettingsView):
    form_class = SettingsForm
    messages = {
                "settings_updated": {
                    "level": messages.SUCCESS,
                    "text": _("Account profile updated.")
                    },
                }

    def get_initial(self):
        initial = super(SettingsView, self).get_initial()
        initial["firstname"] = self.request.user.first_name
        initial["lastname"] = self.request.user.last_name
        uprofile = UProfile.objects.get(user_id=self.request.user)
        initial["birthdate"] = uprofile.birth_date
        initial["github"] = uprofile.github_uname
        initial["about"] = uprofile.about
        return initial

    def update_account(self, form):
        if 'firstname' in form.cleaned_data:
            user = self.request.user
            user.first_name = form.cleaned_data['firstname']
            user.last_name = form.cleaned_data['lastname']
            user.save()
        if 'birthdate' in form.cleaned_data:
            profile, created = UProfile.objects.get_or_create(user=self.request.user)
            profile.birth_date = form.cleaned_data["birthdate"]
            profile.github_uname = form.cleaned_data["github"]
            profile.about = form.cleaned_data["about"]
            profile.save()
        super(SettingsView, self).update_account(form)

    def get_success_url(self, fallback_url=None, **kwargs):
        super(SettingsView, self).get_success_url()
        fallback_url = '/users/{}'.format(self.request.user.username)
        return default_redirect(self.request, fallback_url, **kwargs)

class UProfileView(DetailView):
    template_name = 'userprofile.html'
    model = UProfile
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        slug = self.kwargs['slug']
        user = get_object_or_404(User, username=slug)
        d_obj, create = self.model.objects.get_or_create(user_id=user.id)
        print(d_obj)
        return d_obj

    def get_context_data(self,**kwargs):
        context = super(UProfileView, self).get_context_data(**kwargs)
        context['userdata'] = get_object_or_404(User, username = self.kwargs['slug'])
        context['teams'] = Team.objects.filter(Q(members=self.request.user))
        print(context['teams'][0].event_id)
        return context

class ProfileEventListView(ListView):
    template_name = "userProfileEventList.html"
    queryset = EventRegistration.objects
    context_object_name = 'events'

    def get_queryset(self):
        slug = self.kwargs['slug']
        user = get_object_or_404(User, username=slug)
        queryset = super().get_queryset()
        self.events = queryset.filter(member_id = user.id)
        return self.events

    def get_context_data(self,**kwargs):
        context = super(ProfileEventListView, self).get_context_data(**kwargs)
        context['userdata'] = get_object_or_404(User, username = self.kwargs['slug'])
        return context
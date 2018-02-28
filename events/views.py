from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.http import HttpResponse
from .models import Event
# Create your views here.

class IndexView(ListView):
    template_name = "index.html"
    model = Event
    context_object_name = 'events'

class EventDetailView(DetailView):
    template_name = "eventDetail.html"
    model = Event
    context_object_name = 'event'

class RegisterEventView(DetailView):
    template_name = "eventDetail.html"
    model = Event
    context_object_name = 'event'
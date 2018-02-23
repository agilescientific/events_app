from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from .models import Event
# Create your views here.

class IndexView(TemplateView):
    template_name = "index.html"
    queryset = Event.objects.all()

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['events'] = context['view'].queryset
        return context
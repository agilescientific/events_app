from django.urls import path, re_path

from . import views

urlpatterns = [
    path('users/<slug:slug>', views.UProfileView.as_view(), name='user_detail'),
    path('users/<slug:slug>/events', views.ProfileEventListView.as_view(), name='user_events'),
]
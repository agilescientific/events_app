from django.urls import path, re_path

from . import views

app_name = 'uprofile'

urlpatterns = [
    path('users/<slug:slug>', views.UProfileView.as_view(), name='user_detail'),
    path('users/<slug:slug>/events', views.ProfileEventListView.as_view(), name='user_events'),
    path('users/<slug:slug>/upload_pic/', views.UploadPicture.as_view(), name='profile_upload_pic'),
]
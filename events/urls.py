from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('event/<int:pk>', views.EventDetailView.as_view(), name='event-detail'),
    path('event/<int:pk>/register/', views.RegisterEventView.as_view(), name='event-register')
]
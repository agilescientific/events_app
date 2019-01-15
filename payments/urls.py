from django.urls import path

from . import views

urlpatterns = [
    path('event/<slug:slug>/charge', views.ChargeView.as_view(), name='charge'),
    path('event/<slug:slug>/charge-error', views.ChargeErrorView.as_view(), name='charge-error'),
    path('event/<slug:slug>/payment', views.PayView.as_view(), name='payhome'),
]
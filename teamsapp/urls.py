"""teamsapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.contrib.auth import views as auth_views
from ajax_select import urls as ajax_select_urls

urlpatterns = [
    path('', include('events.urls'), name='home'),
    path('admin/', admin.site.urls),
    path('account/', include("account.urls")),
    path('login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout, name='logout'),
    re_path(r'^ajax_select/', include(ajax_select_urls)),
]

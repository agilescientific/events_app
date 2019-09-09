from background_task import background
from django.contrib.auth.models import User
from .models import GitHubCache, Event
from django.conf import settings
from django.shortcuts import get_object_or_404
from urllib.parse import urlparse
from django.http import JsonResponse
import requests
import json
from django.utils import timezone


@background(schedule=15)
def cache_git(git_id):
    # lookup user by id and send them a message
    git_cache = get_object_or_404(GitHubCache, id=git_id)

    json_r = {}
    zoo_url = git_cache.github
    
    payload = {'client_id':settings.GH_ID, 'client_secret':settings.GH_SECRET}

    repostr = urlparse(zoo_url).path
    
    if repostr[-1]=='/': repostr[:-1]

    repo_url = 'https://api.github.com/repos'+ repostr
    
    issues_r = requests.get(repo_url, params=payload)

    json_r = []
    if issues_r.status_code == 200:
        if issues_r.json()['has_issues']:
            iss_pay = payload
            iss_pay['state'] = 'all'
            issues_r = requests.get(repo_url+'/issues', params=payload)
            json_r.append({'issues':issues_r.json()})
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

    contrib = requests.get(repo_url+'/stats/contributors', params=payload)

    if contrib.status_code < 300:
        json_r.append({'contrib':contrib.json()})
    elif contrib.status_code > 400:
        json_r = {'error' : True}

    daystats = requests.get(repo_url+'/stats/punch_card', params=payload)

    if daystats.status_code == 200:
        json_r.append({'day_stats':daystats.json()})
    elif daystats.status_code > 400:
        json_r = {'error' : True}

    if type(json_r)==list:
        now = timezone.now()
        git_cache.content = json.dumps(json_r)
        git_cache.timestamp = now
        git_cache.save()

    return

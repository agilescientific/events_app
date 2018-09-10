from django.contrib.auth import get_user_model
from django_slack_oauth.models import SlackUser
from django.db import IntegrityError

User = get_user_model()

def register_user(request, api_data):
    if api_data['ok']:
        try:
            user, created = User.objects.get_or_create(
                username=api_data['user']['id'],
                email=api_data['user']['email']
            )
        except IntegrityError:
            print("User name or email already in use!")
            print(api_data['user']['id'], api_data['user']['email'])
            return request, api_data

        if user.is_active:
            slacker, _ = SlackUser.objects.get_or_create(slacker=user)
            slacker.access_token = api_data.pop('access_token')
            slacker.extras = api_data
            slacker.save()

        if created:
            request.created_user = user

    return request, api_data

def debug_oauth_request(request, api_data):
    print(api_data)
    return request, api_data
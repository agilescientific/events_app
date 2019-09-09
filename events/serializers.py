from .models import Idea, Event
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class IdeaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Idea
        # fields = ('url', 'username', 'email', 'groups')
        fields = '__all__'

class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        # fields = ('url', 'username', 'email', 'groups')
        fields = '__all__'

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        # fields = ('url', 'username', 'email', 'groups')
        fields = '__all__'

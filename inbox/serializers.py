# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from dataclasses import field
from pyexpat import model
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import naturaltime


# Internal:
from .models import InboxMessage,Conversation
from profiles.models import Profile
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UserSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField()
    id = serializers.ReadOnlyField()
    class Meta:
        model = User
        fields = ['id', 'username']


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['id',"owner"]


class ConversationBaseSerializer(serializers.ModelSerializer):
    # participants = UserSerializer(many=True, read_only=True)
    participants = UserSerializer(many=True)


    class Meta:
        model=Conversation
        fields = [
            "id","participants","latest_message"
        ]

class InboxMessageSerializer(serializers.ModelSerializer):
    sender=serializers.ReadOnlyField(source="sender.owner.username")
    conversation = serializers.ReadOnlyField(source="conversation.id")
    created_at = serializers.SerializerMethodField()
    # sender = serializers.ReadOnlyField()
    # sender = ProfileSerializer(read_only=True)
    # sender_name = serializers.ReadOnlyField(source="sender.owner.username")

    def get_created_at(self, obj):
        return naturaltime(obj.created_at)
    
    class Meta:
        model = InboxMessage
        fields = [
            "id","conversation","body","created_at","sender","seen"
        ]

    def get_sender(self, obj):
        return {
            'id': obj.sender.owner.id,
            'username': obj.sender.owner.username,
            # Add any other fields you want to include
        }
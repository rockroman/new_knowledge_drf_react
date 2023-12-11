# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from random import choices
from rest_framework import serializers
from django.contrib.humanize.templatetags.humanize import naturaltime



# Internal:
from .models import Profile
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class ProfileBaseSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    first_name = serializers.ReadOnlyField()
    role = serializers.ReadOnlyField()
    role_selected = serializers.ReadOnlyField()
    is_owner = serializers.SerializerMethodField()
    lessons_count = serializers.ReadOnlyField()
    created_on = serializers.SerializerMethodField()
    updated_on = serializers.SerializerMethodField()


    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner
    

    def get_created_on(self, obj):
        return naturaltime(obj.created_on)

    def get_updated_on(self, obj):
        return naturaltime(obj.updated_on)
    
    



    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'first_name', 'last_name',
            'email', 'bio', 'role', 'created_on', 'updated_on',
            'image', 'role_selected', 'is_owner', "lessons_count",
            ]
        

class RoleSelectionSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=Profile.ROLE)

    class Meta:
        model = Profile
        fields = ['role']
        




# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from random import choices
from rest_framework import serializers


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

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

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
        




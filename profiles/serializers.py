# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from rest_framework import serializers


# Internal:
from .models import Profile
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class ProfileBaseSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    role = serializers.ReadOnlyField()
    role_selected = serializers.ReadOnlyField()

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'first_name', 'last_name',
            'email', 'bio', 'role', 'created_on', 'updated_on',
            'image', 'role_selected'
            ]
        




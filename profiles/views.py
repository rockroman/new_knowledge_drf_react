# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

# Internal:
from .models import Profile
from .serializers import ProfileBaseSerializer
from profiles import serializers
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class ProfileList(APIView):
    """
    listing all user profiles
    """
    def get(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileBaseSerializer(profiles, many=True)
        return Response (serializer.data)


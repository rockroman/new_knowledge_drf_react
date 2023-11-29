# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.shortcuts import render
from django.http import Http404
from django.urls import is_valid_path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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
    
class ProfileDetail(APIView):
    serializer_class = ProfileBaseSerializer
    def get_object(self, pk):
        try:
            profile = Profile.objects.get(pk=pk)
            return profile
        except Profile.DoesNotExist:
            raise Http404
        
    def get(self, request, pk):
        profile = self.get_object(pk)
        serializer = ProfileBaseSerializer(profile)
        return Response(serializer.data)
    
    def put(self, request, pk):
        profile = self.get_object(pk=pk)
        serializer = ProfileBaseSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        




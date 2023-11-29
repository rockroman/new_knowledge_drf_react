# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from multiprocessing import context
from django.shortcuts import render
from django.http import Http404
from django.urls import is_valid_path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

# Internal:
from .models import Profile
from .serializers import ProfileBaseSerializer,RoleSelectionSerializer
# from profiles import serializers
from knowledge_API.permissions import CanSetRole, IsOwnerOrReadOnly,CanSetRole
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@api_view(['GET','PUT'])
@permission_classes([IsAuthenticated,CanSetRole])
def set_role_view(request):
    #  user has a profile (created by a signal)
    
    # Check if the profile already has a role set
    profile = request.user.profile
    if request.method == 'GET':
        # Return 200 if the user doesn't have a role set
        if not profile.role:
            return Response({'detail': 'User does not have a role set'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Role is already set'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = RoleSelectionSerializer(data=request.data, instance=profile)
    if serializer.is_valid():
        role = serializer.validated_data['role']
        profile.role = role
        profile.rolle_selected = True
        profile.save()
        return Response({'detail': 'Role set successfully'}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileList(APIView):
    """
    listing all user profiles
    """
    def get(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileBaseSerializer(profiles, many=True, context={'request':request})
        return Response (serializer.data)
    
class ProfileDetail(APIView):
    serializer_class = ProfileBaseSerializer
    permission_classes = [IsOwnerOrReadOnly]
    def get_object(self, pk):
        try:
            profile = Profile.objects.get(pk=pk)
            return profile
        except Profile.DoesNotExist:
            raise Http404
        
    def get(self, request, pk):
        profile = self.get_object(pk)
        self.check_object_permissions(self.request,profile)
        serializer = ProfileBaseSerializer(profile, context={'request':request})
        return Response(serializer.data)
    
    def put(self, request, pk):
        profile = self.get_object(pk=pk)
        serializer = ProfileBaseSerializer(profile, data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        




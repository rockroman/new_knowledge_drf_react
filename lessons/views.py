

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from multiprocessing import context
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from django.http import Http404

import lessons


# Internal:
from .models import Lesson
from .serializers import LessonsBaseSerializer
from lessons import serializers
from knowledge_API.permissions import IsOwnerOrReadOnly, RoleOnProfileIsSet

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class LessonsList(APIView):
    serializer_class=LessonsBaseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self,request):
        lessons = Lesson.objects.all()

        serializer = LessonsBaseSerializer(lessons,many=True, context={'request':request})
        return Response (serializer.data)
    
    def post(self,request):
        if request.user.profile.role != 'Mentor':
            return Response({'detail': 'Only mentors can create lessons.'}, status=status.HTTP_403_FORBIDDEN)
        
        
        serializer = LessonsBaseSerializer(
            data=request.data, context={'request':request}
        )
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class LessonDetail(APIView):
    permission_classes = [IsOwnerOrReadOnly,RoleOnProfileIsSet]
    serializer_class=LessonsBaseSerializer
    def get_object(self,pk):
        try:
            lesson = Lesson.objects.get(pk=pk)
            self.check_object_permissions(self.request,lesson)
            self.check_permissions(self.request)
            return lesson
        except Lesson.DoesNotExist:
            raise Http404
        
    def get(self, request, pk):
        lesson = Lesson.objects.get(pk=pk)
        serializer = LessonsBaseSerializer(lesson, context={'request':request})
        return Response(serializer.data)
    
    def put(self,request,pk):
        lesson = self.get_object(pk)
        serializer = LessonsBaseSerializer(
            lesson, data=request.data,context={'request':request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



        

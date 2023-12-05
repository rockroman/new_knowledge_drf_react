

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from multiprocessing import context
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions


# Internal:
from .models import Lesson
from .serializers import LessonsBaseSerializer
from lessons import serializers

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class LessonsList(APIView):
    serializer_class=LessonsBaseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self,request):
        lessons = Lesson.objects.all()
        print(request.user.profile.role)
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

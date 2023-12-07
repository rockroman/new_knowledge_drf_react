
# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.shortcuts import render
from rest_framework import generics,permissions

from knowledge_API.permissions import IsOwnerOrReadOnly, RoleOnProfileIsSet


# Internal:
from .models import Comment
from .serializers import CommentSerializer, CommentDetailSerializer

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,RoleOnProfileIsSet]
    queryset = Comment.objects.all()

    # associate user with comment
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly,RoleOnProfileIsSet]
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.all()
 
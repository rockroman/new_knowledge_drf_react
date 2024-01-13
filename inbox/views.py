# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:

from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from   django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status,generics,filters
from rest_framework.views import APIView

from inbox import serializers
from knowledge_API.permissions import IsOwnerOrReadOnly, RoleOnProfileIsSet

from django.db.models import Q
from django.db.models import Case, When, Value, IntegerField
from django.db.models.functions import Lower


# Internal:
from .models import Conversation,InboxMessage
from .serializers import ConversationBaseSerializer,InboxMessageSerializer,ProfileSerializer, UserSerializer
from profiles.serializers import ProfileBaseSerializer

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    
class InboxView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated & RoleOnProfileIsSet]
    serializer_class = ConversationBaseSerializer

    def get_queryset(self):
        return (
            Conversation.objects
            .filter(participants=self.request.user)
            .annotate(
                is_current_user_participant=Case(
                    When(participants=self.request.user, then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            )
            .order_by('-is_current_user_participant')
        )
    

    def post(self, request, *args, **kwargs):
        print("current user in post", self.request.user)
        # Extract the participants list from the request data
        participants_data = request.data.get('participants', [])
        print(participants_data)

        # Validate that the participants list contains exactly one participant
        if len(participants_data) != 1:
            return Response({'error': 'Exactly one participant is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Extract the username of the other participant
        other_participant_username = participants_data[0].get('username')

        # Get or create a conversation with the current user and the other participant
        print("current user before con exists check", self.request.user)
        existing_conversation = Conversation.objects.filter(participants__username=other_participant_username,participants=request.user)
        print(existing_conversation,"filtering existing conv")
        print(Conversation.objects.all())
        if existing_conversation.exists():
            serializer = ConversationBaseSerializer(existing_conversation.first(), context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        new_conversation = Conversation.objects.create()
        try:
            other_participant = User.objects.get(username=other_participant_username)
            new_conversation.participants.add(request.user, other_participant)
        except User.DoesNotExist:
            # If the other participant is not found, you can create a new User instance here
            return Response({'error': f'Participant with username {other_participant_username} not found'}, status=status.HTTP_400_BAD_REQUEST)
        except User.MultipleObjectsReturned:
            return Response({'error': f'Multiple users found with username {other_participant_username}'}, status=status.HTTP_400_BAD_REQUEST)

        # Add the current user to the conversation
        print("curr user before adding to new conv",self.request.user)
        new_conversation.participants.add(request.user)

        serializer = ConversationBaseSerializer(new_conversation, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)




class ConversationDetailView(APIView):
    permission_classes = [IsAuthenticated,RoleOnProfileIsSet]
    def get(self, request, conversation_id):
        conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
        messages_data = conversation.messages.all()
        for message in messages_data:
            if message.sender != request.user.profile:
                message.seen = True
                message.save()

        serializer = InboxMessageSerializer(messages_data, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, conversation_id):
        conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
        
        #  'body' field in your request data containing the message body
        message_body = request.data.get('body', '')

        # Create a new message
        new_message = InboxMessage.objects.create(
            sender=request.user.profile,  # Assuming sender is the user's profile
            conversation=conversation,
            body=message_body
        )

        # Serialize the new message for the response
        serializer = InboxMessageSerializer(new_message)

        return Response(serializer.data)
    

class UserSearchList(generics.ListAPIView):
    permission_classes = [IsAuthenticated & RoleOnProfileIsSet]
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by(Lower("username"))
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["username"]


        


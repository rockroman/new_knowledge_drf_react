# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
import imp
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from inbox import serializers
from knowledge_API.permissions import IsOwnerOrReadOnly, RoleOnProfileIsSet


# Internal:
from .models import Conversation,InboxMessage
from .serializers import ConversationBaseSerializer,InboxMessageSerializer,ProfileSerializer
from profiles.serializers import ProfileBaseSerializer

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])

# def inbox_view(request):
    
#     user_conversations = Conversation.objects.all()
#     serializer = ConversationBaseSerializer(user_conversations,many=True,context={'request':request})
#     return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated,RoleOnProfileIsSet])
def inbox_view(request):
    
    user_conversations = Conversation.objects.filter(participants=request.user)
    serializer = ConversationBaseSerializer(user_conversations,many=True,context={'request':request})
    return Response(serializer.data)


# @permission_classes([IsAuthenticated])
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
        
        # Assuming you have a 'body' field in your request data containing the message body
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


# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def conversation_detail(request, conversation_id):
#     conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)

#     if request.method == "GET":
#         messages_data = conversation.messages.all()
#         serializer = InboxMessageSerializer(messages_data, many=True, context={'request': request})
#         return Response(serializer.data)
    
#     elif request.method == "POST":
#         conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
        
#         # Assuming you have a 'body' field in your request data containing the message body
#         message_body = request.data.get('body', '')

#         # Create a new message
#         new_message = InboxMessage.objects.create(
#             sender=request.user.profile,  # Assuming sender is the user's profile
#             conversation=conversation,
#             body=message_body
#         )

#         # Serialize the new message for the response
#         serializer = InboxMessageSerializer(new_message)

#         return Response(serializer.data)





# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def conversation_detail(request, conversation_id):
#     conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)

#     if request.method == "GET":
#         # Serialize the entire conversation
#         serializer = ConversationBaseSerializer(conversation, context={'request': request})
#         conversation_data = serializer.data

#         # Include details of individual messages
#         conversation_data['messages'] = InboxMessageSerializer(conversation.messages.all(), many=True, context={'request': request}).data

#         return Response(conversation_data)
    
#     elif request.method == "POST":
#         conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
        
#         # Assuming you have a 'body' field in your request data containing the message body
#         message_body = request.data.get('body', '')

#         # Create a new message
#         new_message = InboxMessage.objects.create(
#             sender=request.user.profile,  # Assuming sender is the user's profile
#             conversation=conversation,
#             body=message_body
#         )

#         # Serialize the new message for the response
#         serializer = InboxMessageSerializer(new_message)

#         return Response(serializer.data)

# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def conversation_detail(request, conversation_id):
#     conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)

#     if request.method == "GET":
#         # Serialize the entire conversation
#         conversation_serializer = ConversationBaseSerializer(conversation, context={'request': request})
#         conversation_data = conversation_serializer.data

#         # Include details of individual messages
#         messages_serializer = InboxMessageSerializer(conversation.messages.all(), many=True, context={'request': request})
#         conversation_data['messages'] = messages_serializer.data

#         return Response(conversation_data)
    
#     elif request.method == "POST":
#         conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
        
#         # Assuming you have a 'body' field in your request data containing the message body
#         message_body = request.data.get('body', '')

#         # Create a new message
#         new_message = InboxMessage.objects.create(
#             sender=request.user.profile,  # Assuming sender is the user's profile
#             conversation=conversation,
#             body=message_body
#         )

#         # Serialize the new message for the response
#         serializer = InboxMessageSerializer(new_message)

#         return Response(serializer.data)

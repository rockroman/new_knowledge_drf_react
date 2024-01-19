# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
import json
from django.db import models
from django.contrib.auth.models import User
from pytz import timezone
from django.core.serializers import serialize


# Internal:
from profiles.models import Profile

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class Conversation(models.Model):
    participants = models.ManyToManyField(User,related_name='conversations')
    latest_message = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-latest_message"]
    
    def __str__(self) -> str:
        user_names = ",".join(user.username for user in self.participants.all())
        return f'[{user_names}]'
    def participants_list(self):
            return [{'id': user.id, 'username': user.username} for user in self.participants.all()]


class InboxMessage(models.Model):
    sender = models.ForeignKey(Profile,on_delete=models.CASCADE, related_name='sent_messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE,related_name='messages')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    class Meta:
        ordering=["created_at"]
    
    def __str__(self) -> str:
        return f'{ self.sender.owner}'

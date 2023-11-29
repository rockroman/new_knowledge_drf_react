# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Internal:
from .models import Profile

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



@receiver(post_save, sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        profile = Profile.objects.create(owner=instance)
        # assigning the newly created user username and email 
        # to profile fields
        profile.first_name = instance.username
        profile.email = instance.email
        profile.save()


@receiver(post_save,sender=Profile)
def updating_user_profile(sender,instance, created, **kwargs):
        if not created:
            user_instance = instance.owner
            user_instance.email = instance.email
            user_instance.save()



               
          
          

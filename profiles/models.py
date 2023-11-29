# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """
    Profile for each registered user
    """
    ROLE = (
    ('Mentor', 'Mentor'),
    ('Student', 'Student')

    )

    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=100)
    bio = models.TextField(max_length=1000, blank=True)
    role = models.CharField(max_length=20, choices=ROLE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    image = models.ImageField (
        upload_to="images/", default="images/default_profile_gwcpmq"
    )
    role_selected = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self) -> str:
        return f"{self.owner}'s profile"
    
    def save(self, *args, **kwargs):
        if self.role and not self.role_selected:
            self.role_selected = True

        super().save(*args, **kwargs)
    


    
# @receiver(post_save, sender=User)
# def create_user_profile(sender,instance,created,**kwargs):
#     if created:
#         profile = Profile.objects.create(owner=instance)
#         # assigning the newly created user username and email 
#         # to profile fields
#         profile.first_name = instance.username
#         profile.email = instance.email
#         profile.save()

# @receiver(post_save,sender=Profile)
# def updating_user_profile(sender,instance, created, **kwargs):
#         if not created:
#             user_instance = instance.owner
#             user_instance.email = instance.email
#             user_instance.save()




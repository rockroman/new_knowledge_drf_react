from django import views
from django.urls import path
from .views import ProfileList

urlpatterns = [
    path('profiles/',ProfileList.as_view(), name='profiles' ),
]
from django import views
from django.urls import path
from .views import ProfileList, ProfileDetail, set_role_view

urlpatterns = [
    path('profiles/',ProfileList.as_view(), name='profiles' ),
    path('profile/<int:pk>/',ProfileDetail.as_view(), name='profile' ),
     path('set_role/', set_role_view, name='set_role'),
    
]
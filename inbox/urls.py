from django.contrib import admin
from django.urls import path, include
import rest_framework
from inbox import views 

urlpatterns = [
    path('inbox/',views.InboxView.as_view() ),
    path('inbox/conversation/<int:conversation_id>',views.ConversationDetailView.as_view() ),
    path('inbox/users_search',views.UserSearchList.as_view() ),

   
]

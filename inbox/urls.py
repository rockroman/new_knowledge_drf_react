from django.contrib import admin
from django.urls import path, include
import rest_framework
from inbox import views 

urlpatterns = [
    path('inbox/',views.inbox_view ),
    # path('inbox/conversation/<int:conversation_id>',views.conversation_detail ),
    path('inbox/conversation/<int:conversation_id>',views.ConversationDetailView.as_view() ),

   
]

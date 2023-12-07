from django.contrib import admin
from django.urls import path, include

from comments import views 

urlpatterns = [
    path('comments/',views.CommentList.as_view() ),
    path('comment/<int:pk>/',views.CommentDetail.as_view() ),
    # path('inbox/conversation/<int:conversation_id>',views.conversation_detail ),
    # path('inbox/conversation/<int:conversation_id>',views.ConversationDetailView.as_view() ),

   
]

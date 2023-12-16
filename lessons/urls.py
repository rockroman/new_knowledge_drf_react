


from django.contrib import admin
from django.urls import path, include
import rest_framework
from lessons import views 

urlpatterns = [
    path('lessons/',views.LessonsList.as_view() ),
    path('lesson/<int:pk>',views.LessonDetail.as_view() ),
    path('categories/',views.LearningCategoryList.as_view() ),
   
]

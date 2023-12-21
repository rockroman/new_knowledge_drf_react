# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from pyexpat import model
from random import choices
from urllib import request
from rest_framework import serializers
from django.contrib.humanize.templatetags.humanize import naturaltime


# Internal:
from .models import LearningCategory, Lesson
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class LessonsBaseSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source="author.profile.id")
    profile_image = serializers.ReadOnlyField(source="author.profile.image.url")
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    comments_count = serializers.ReadOnlyField()

    def validate_image(self,value):
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                "cant upload images larger than 2MB in size"
            )
        
        if value.image.height > 2000:
            raise serializers.ValidationError(
                "Image height larger than 2000px"
            )
        
        if value.image.width > 2000:
            raise serializers.ValidationError(
            "Image width larger than 2000px"
        )
        return value

            

    def get_is_owner(self,obj):
        request = self.context["request"]
        return request.user == obj.author
    
    def get_created_at(self, obj):
        return naturaltime(obj.created_at)

    def get_updated_at(self, obj):
        return naturaltime(obj.updated_at)
    

    class Meta:
        model = Lesson
        fields = [
            "id","author","is_owner","profile_id","profile_image",
            "category","title","content","image",
            "external_resources","learning_instructions", "created_at",
            "updated_at","comments_count",
           
        ]

class LearningCategorySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    created_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return naturaltime(obj.created_at)


    class Meta:
        model = LearningCategory
        fields = [
            'id','owner','name','category_image',
            'body', 'created_at'
        ]
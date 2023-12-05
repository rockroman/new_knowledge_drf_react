# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from random import choices
from urllib import request
from rest_framework import serializers


# Internal:
from .models import LearningCategory, Lesson
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class LessonsBaseSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source="author.profile.id")
    profile_image = serializers.ReadOnlyField(source="author.profile.image.url")

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
    

    class Meta:
        model = Lesson
        fields = [
            "id","author","is_owner","profile_id","profile_image",
            "category","title","content","image",
            "external_resources","learning_instructions",
           
        ]
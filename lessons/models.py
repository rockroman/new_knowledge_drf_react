
# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from ast import mod
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.template.defaultfilters import slugify


# Internal:
from profiles.models import Profile

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



class LearningCategory(models.Model):
    owner =  models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=50)
    category_image = CloudinaryField('image', default='placeholder')
    body = models.TextField()
    created_at = models.DateTimeField()

    def __str__(self) -> str:
        return  self.name 
 




class Lesson (models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=200, unique=True)
    category = models.ForeignKey(LearningCategory, on_delete=models.PROTECT,related_name='user_learning_category')
    content = models.TextField()
    image = models.ImageField(upload_to="images/", default="/default_post_gfksyz",
        blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    external_resources = models.URLField(blank=True)
    learning_instructions = models.CharField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.title + ' | ' + str(self.author)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


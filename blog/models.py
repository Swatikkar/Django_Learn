from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profilepic = models.ImageField(upload_to='profile_pics', blank=True)
    full_name = models.CharField(max_length=150,blank=True)

class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_pics', blank=True)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




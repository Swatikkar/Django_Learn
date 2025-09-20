from django.contrib import admin

# Register your models here.
from .models import UserProfile, Posts

admin.site.register(UserProfile)
admin.site.register(Posts)

from django.contrib import admin

# Register your models here.
from .models import UserProfile

# class UserProfile(admin.ModelAdmin):
#     list_display=[
#         'telephone',
#     ]

admin.site.register(UserProfile)
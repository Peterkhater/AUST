from django.contrib import admin
from django.contrib.auth.models import User
from .models import CustomUser,Profile

admin.site.register(User)
admin.site.register(CustomUser)
admin.site.register(Profile)

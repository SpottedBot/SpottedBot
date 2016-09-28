from django.contrib import admin

# Register your models here.
from .models import Spotted, Profile
admin.site.register(Spotted)
admin.site.register(Profile)

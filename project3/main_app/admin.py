from django.contrib import admin
from .models import Category, CustomUser, UserCategory, Quiz

admin.site.register(Category)
admin.site.register(CustomUser)
admin.site.register(UserCategory)
admin.site.register(Quiz)

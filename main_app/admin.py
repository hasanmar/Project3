from django.contrib import admin
from .models import Category, CustomUser, UserCategory, Exercise, Quiz


admin.site.register(Category)
admin.site.register(CustomUser)
admin.site.register(UserCategory)

admin.site.register(Quiz)

admin.site.register(Exercise)


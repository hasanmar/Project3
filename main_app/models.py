from django.conf import settings
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.contrib import admin


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=700)
    imagePath = models.CharField(max_length=100,
                                 default='images/categories/1.png',
                                 blank=True)

    def get_absolute_url(self):
        return reverse("Category_detail", kwargs={"pk": self.id})

    def __str__(self):
        return self.name


    #Category, through='UserCategory',
class CustomUser(AbstractUser, models.Model):
    email = models.EmailField(max_length=255, blank=False, default='')
    level = models.FloatField(default=0)
    image = models.ImageField(upload_to='images/profile_images', default='im', blank=True)

    def __str__(self):
        return self.username


class UserCategory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    level = models.FloatField(default=0)
    attempts = models.IntegerField(default=0)


class Exercise(models.Model):
    question = models.TextField(max_length=500)
    option1 = models.CharField(max_length=150)
    option2 = models.CharField(max_length=150)
    option3 = models.CharField(max_length=150)
    option4 = models.CharField(max_length=150)
    correctAnswer = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    isApproved = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)

    def get_absolute_url(self):
        return reverse("contribute")


class Quiz(models.Model):
    qustion = models.TextField(max_length=500)
    option1 = models.CharField(max_length=150)
    option2 = models.CharField(max_length=150)
    option3 = models.CharField(max_length=150)
    option4 = models.CharField(max_length=150)
    correctAnswer = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    isApproved = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)


    def get_absolute_url(self):
        return reverse("contribute")
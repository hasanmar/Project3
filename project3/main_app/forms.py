from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser, Exercise, User


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


## Add Exercises ##

class AddExerciseForm(forms.ModelForm):
    body = forms.CharField(required=True)
    
    class Meta:
        model = Exercise
        fields = ['question', 'option1', 'option2', 'option3', 'option4', 'correctAnswer']

## Add Exercises ##   
        